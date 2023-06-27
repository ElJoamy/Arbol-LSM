import time
import pickle
from sortedcontainers import SortedDict
import zlib
import os
import shutil
from dotenv import load_dotenv

load_dotenv()

class LSMTree:
    def __init__(self, threshold=100, compression=True, db_path=os.getenv('DB_PATH')):
        self.threshold = threshold
        self.compression = compression
        self.memtable = {}
        self.sstables = []
        self.db_path = os.path.abspath(db_path)
        self.index = {}
        os.makedirs(self.db_path, exist_ok=True)

    def put(self, key, value, ttl=None):
        self.memtable[key] = {'value': value, 'timestamp': time.time(), 'ttl': ttl}

        if len(self.memtable) >= self.threshold:
            self.flush_memtable()

    def get(self, key):
        if key in self.memtable:
            entry = self.memtable[key]
            if self.is_entry_valid(entry):
                return entry['value']
            else:
                del self.memtable[key]

        if key in self.index:
            sstable_index, sstable_key = self.index[key]
            sstable = self.sstables[sstable_index]
            entry = sstable[sstable_key]
            if self.is_entry_valid(entry):
                return entry['value']
            else:
                del sstable[sstable_key]
                del self.index[key]

        return None

    def is_entry_valid(self, entry):
        if entry['ttl'] is not None and (time.time() - entry['timestamp']) >= entry['ttl']:
            return False
        return True

    def flush_memtable(self):
        self.sstables.append(self.memtable)
        self.index_memtable()

        self.memtable = {}

        if self.compression:
            self.compress_sstable(self.sstables[-1])

        self.merge_sstables()

    def compress_sstable(self, sstable):
        for key, entry in sstable.items():
            compressed_value = zlib.compress(entry['value'].encode())
            entry['value'] = compressed_value

    def merge_sstables(self):
        if len(self.sstables) > 1:
            merged_sstable = {}

            for sstable in self.sstables:
                for key, entry in sstable.items():
                    merged_sstable[key] = entry

            self.sstables = [merged_sstable]

    def index_memtable(self):
        for key in self.memtable:
            self.index[key] = (len(self.sstables), key)

    def persist_sstables(self):
        new_db_path = f'{self.db_path}_new'

        if not os.path.exists(new_db_path):
            os.makedirs(new_db_path)

        for i, sstable in enumerate(self.sstables):
            filename = f'{new_db_path}/sstable_{i}.txt'

            with open(filename, 'w') as file:
                for key, entry in sstable.items():
                    file.write(f'{key},{entry["value"]},{entry["timestamp"]},{entry["ttl"]}\n')

        shutil.rmtree(self.db_path)
        shutil.move(new_db_path, self.db_path)

        self.sstables = []

    def load_sstables(self):
        if not os.path.exists(self.db_path):
            return

        self.sstables = []

        for filename in os.listdir(self.db_path):
            sstable = {}

            with open(f'{self.db_path}/{filename}', 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    key = parts[0]
                    value = parts[1]
                    timestamp = float(parts[2])
                    ttl = float(parts[3])

                    sstable[key] = {'value': value, 'timestamp': timestamp, 'ttl': ttl}

            self.sstables.append(sstable)

        self.build_index()

    def build_index(self):
        self.index = {}

        for i, sstable in enumerate(self.sstables):
            for key in sstable:
                self.index[key] = (i, key)

    def save_to_disk(self, filepath):
        with open(filepath, 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def load_from_disk(filepath):
        with open(filepath, 'rb') as file:
            return pickle.load(file)

    def close(self):
        self.persist_sstables()
        self.memtable = {}
        self.sstables = []
        self.index = {}