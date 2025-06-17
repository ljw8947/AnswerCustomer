import csv
import os

class CsvManager:
    def __init__(self, file_path, model_class):
        self.file_path = file_path
        self.model_class = model_class
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.file_path) or '.', exist_ok=True)
            with open(self.file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Write header row based on model_class's expected attributes
                if hasattr(self.model_class, 'to_dict'):
                    # Create a dummy instance to get attribute names, or assume a fixed header
                    # A more robust solution might require a defined HEADERS class attribute in models
                    if self.model_class.__name__ == "Issue":
                        writer.writerow(['issue_id', 'create_time', 'carline', 'power', 'specific_function', 'function_domain', 'general_domain', 'issue_type', 'description', 'description_en', 'brief_issue', 'brief_issue_en', 'global_id', 'user_issue_id', 'created_by_user_id', 'status', 'assigned_to_user_id', 'extra_info', 'notified'])
                    elif self.model_class.__name__ == "User":
                        writer.writerow(['username', 'email', 'password_hash', 'role', 'status', 'user_id'])

    def read_all(self):
        data = []
        if not os.path.exists(self.file_path):
            return data
        with open(self.file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(self.model_class.from_dict(row))
        return data

    def write_all(self, items):
        if not items:
            # If no items, ensure file still has headers if it exists, or create with headers
            self._ensure_file_exists()
            return

        # Get header from the first item if items exist, assuming they are model instances
        header = list(items[0].to_dict().keys())
        
        with open(self.file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            for item in items:
                writer.writerow(item.to_dict())

    def add_item(self, item):
        items = self.read_all()
        items.append(item)
        self.write_all(items)

    def get_item_by_id(self, item_id, id_field_name):
        items = self.read_all()
        for item in items:
            if getattr(item, id_field_name) == item_id:
                return item
        return None

    def update_item(self, item_id, updated_item, id_field_name):
        items = self.read_all()
        found = False
        for i, item in enumerate(items):
            if getattr(item, id_field_name) == item_id:
                items[i] = updated_item
                found = True
                break
        if found:
            self.write_all(items)
        return found

    def delete_item(self, item_id, id_field_name):
        items = [item for item in self.read_all() if getattr(item, id_field_name) != item_id]
        self.write_all(items)
        return True 