import ui
import os
import csv
from datetime import datetime
import dialogs

# Setup file paths in the iOS Documents directory
FILE_DIR = os.path.expanduser('~/Documents/expense_tracker')
FILE_PATH = os.path.join(FILE_DIR, 'expenses.csv')
HEADERS = ['date', 'type', 'category', 'amount', 'description']

def init_file():
    """Ensure the folder and CSV file exist, creating it if necessary."""
    if not os.path.exists(FILE_DIR):
        os.makedirs(FILE_DIR)
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)

def load_entries():
    """Read all entries from CSV and return as a list of dicts."""
    entries = []
    try:
        with open(FILE_PATH, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                entries.append(row)
    except FileNotFoundError:
        pass
    return entries

def save_entry(entry):
    """Append a single entry (dict) to the CSV."""
    with open(FILE_PATH, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writerow(entry)

class TrackerApp:
    def __init__(self):
        screen_w, screen_h = ui.get_screen_size()
        self.main_view = ui.View(frame=(0, 0, screen_w, screen_h))
        self.main_view.name = 'Expense Tracker'
        self.main_view.background_color = 'white'

        self.segment = ui.SegmentedControl(frame=(10, 30, screen_w - 20, 30))
        self.segment.segments = ['Add Entry', 'View Entries', 'Summary']
        self.segment.action = self.switch_tab
        self.segment.flex = 'W'
        self.segment.tint_color = '#007AFF'  # iOS blue tint
        self.main_view.add_subview(self.segment)

        content_y = self.segment.y + self.segment.height + 10
        content_h = screen_h - content_y - 10

        self.v_add = ui.View(frame=(0, content_y, screen_w, content_h))
        self.v_list = ui.View(frame=self.v_add.frame)
        self.v_summary = ui.View(frame=self.v_add.frame)

        for v in (self.v_add, self.v_list, self.v_summary):
            v.flex = 'WH'
            v.background_color = 'white'
            self.main_view.add_subview(v)

        self.setup_add_tab()
        self.setup_list_tab()
        self.setup_summary_tab()

        self.switch_tab()

    def setup_add_tab(self):
        v = self.v_add
        v.flex = 'WH'
        y = 10
        labels = ['Type (income/expense):', 'Category:', 'Amount:', 'Description (opt):']
        names = ['t_type', 't_cat', 't_amt', 't_desc']

        self.fields = {}

        for lbl_text, name in zip(labels, names):
            label = ui.Label(frame=(10, y, v.width - 20, 30))
            label.text = lbl_text
            label.text_color = 'black'
            label.flex = 'W'
            v.add_subview(label)

            tf = ui.TextField(frame=(10, y + 30, v.width - 20, 35))
            tf.border_style = 1  # rounded border
            tf.background_color = 'white'
            tf.text_color = 'black'
            tf.flex = 'W'
            if name == 't_amt':
                tf.keyboard_type = 2  # numbers & punctuation keyboard
            setattr(self, name, tf)
            self.fields[name] = tf
            v.add_subview(tf)
            y += 80

        btn = ui.Button(frame=(10, y, v.width - 20, 45))
        btn.title = 'Add Entry'
        btn.action = self.do_add_entry
        btn.flex = 'W'
        btn.background_color = '#007AFF'
        btn.tint_color = 'white'
        v.add_subview(btn)

    def do_add_entry(self, sender):
        etype = self.t_type.text.strip().lower()
        cat = self.t_cat.text.strip()
        amt = self.t_amt.text.strip()
        desc = self.t_desc.text.strip()

        if etype not in ('income', 'expense'):
            dialogs.alert('Error', "Type must be 'income' or 'expense'", 'OK')
            return
        if not cat:
            dialogs.alert('Error', "Category is required", 'OK')
            return
        try:
            amt_f = float(amt)
        except:
            dialogs.alert('Error', "Amount must be a number", 'OK')
            return

        entry = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'type': etype,
            'category': cat,
            'amount': f'{amt_f:.2f}',
            'description': desc
        }
        save_entry(entry)

        # Clear form
        for tf in self.fields.values():
            tf.text = ''

        # Show alert with delay to avoid blocking UI immediately
        def show_success():
            dialogs.alert('Success', 'Entry added!', 'OK')
            # Refresh list only if View Entries tab is active
            if self.segment.selected_index == 1:
                self.refresh_list()

        ui.delay(show_success, 0.1)


    def setup_list_tab(self):
        v = self.v_list
        v.flex = 'WH'

        self.table = ui.TableView(frame=(10, 10, v.width - 20, v.height - 70))
        self.table.flex = 'WH'
        self.table.data_source = self
        self.table.delegate = self
        self.table.background_color = 'white'
        v.add_subview(self.table)

        self.btn_delete = ui.Button()
        self.btn_delete.title = 'Delete Selected'
        self.btn_delete.action = self.do_delete
        self.btn_delete.background_color = '#FF3B30'
        self.btn_delete.tint_color = 'white'
        self.btn_delete.flex = 'W'
        v.add_subview(self.btn_delete)

        # Set button frame in layout method
        def layout(_):
            self.table.frame = (10, 10, v.width - 20, v.height - 70)
            self.btn_delete.frame = (10, v.height - 50, v.width - 20, 40)
        v.set_needs_layout()
        v.layout = layout

        self.refresh_list()


    def refresh_list(self):
        self.entries = load_entries()
        self.table.reload()
        self.selected_row = None

    def tableview_number_of_rows(self, tv, section):
        return len(self.entries)

    def tableview_cell_for_row(self, tv, section, row):
        cell = ui.TableViewCell()
        e = self.entries[row]
        cell.background_color = 'white'
        cell.text_label.text_color = 'black'
        cell.text_label.text = f"{e['date']} | {e['type']} | {e['category']} | ${e['amount']} | {e['description']}"
        return cell

    def tableview_did_select(self, tv, section, row):
        self.selected_row = row

    def do_delete(self, sender):
        if self.selected_row is None:
            dialogs.alert('Warning', 'No entry selected', 'OK')
            return
        idx = self.selected_row
        confirm = dialogs.confirm_alert('Confirm', 'Delete selected entry?', 'Yes', 'No')
        if not confirm:
            return

        self.entries.pop(idx)
        with open(FILE_PATH, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=HEADERS)
            writer.writeheader()
            writer.writerows(self.entries)
        dialogs.alert('Success', 'Entry deleted', 'OK')
        self.refresh_list()

    def setup_summary_tab(self):
        v = self.v_summary
        v.flex = 'WH'

        self.summary_view = ui.TextView(frame=(10, 10, v.width - 20, v.height - 20))
        self.summary_view.editable = False
        self.summary_view.flex = 'WH'
        self.summary_view.background_color = 'white'
        self.summary_view.text_color = 'black'
        v.add_subview(self.summary_view)

    def show_summary(self):
        entries = load_entries()
        income, expense = 0.0, 0.0
        for e in entries:
            try:
                a = float(e['amount'])
            except:
                a = 0.0
            if e['type'] == 'income':
                income += a
            elif e['type'] == 'expense':
                expense += a
        bal = income - expense
        txt = (
            f"Total Income: ${income:.2f}\n"
            f"Total Expense: ${expense:.2f}\n"
            f"Current Balance: ${bal:.2f}\n"
        )
        self.summary_view.text = txt

    def switch_tab(self, sender=None):
        idx = self.segment.selected_index
        self.v_add.hidden = idx != 0
        self.v_list.hidden = idx != 1
        self.v_summary.hidden = idx != 2
        if idx == 1:
            self.refresh_list()
        elif idx == 2:
            self.show_summary()

    def run(self):
        init_file()
        self.main_view.present('fullscreen')

if __name__ == '__main__':
    TrackerApp().run()
