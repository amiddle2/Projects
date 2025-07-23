import ui
import os
import csv
from datetime import datetime
import dialogs
from collections import defaultdict

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

def write_all_entries(entries):
    """Overwrite CSV with given entries."""
    with open(FILE_PATH, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(entries)

class TrackerApp:
    def __init__(self):
        # Main container view with multiple subviews
        self.main_view = ui.View(frame=(0, 0, 375, 667))
        self.main_view.name = 'Expense Tracker'
        self.main_view.background_color = '#121212'  # dark background
        
        # Top segment controller to switch tabs
        self.segment = ui.SegmentedControl(frame=(10, 30, 355, 30))
        self.segment.segments = ['Add Entry', 'View Entries', 'Summary']
        self.segment.action = self.switch_tab
        self.segment.tint_color = 'white'
        self.main_view.add_subview(self.segment)
        
        # Create each tab view
        self.v_add = ui.View(frame=self.main_view.bounds.inset(0, 70, 0, 0))
        self.v_list = ui.View(frame=self.v_add.frame)
        self.v_summary = ui.View(frame=self.v_add.frame)
        
        for v in (self.v_add, self.v_list, self.v_summary):
            v.background_color = '#121212'
            self.main_view.add_subview(v)
        
        self.editing_index = None  # Track editing mode
        
        self.setup_add_tab()
        self.setup_list_tab()
        self.setup_summary_tab()
        
        self.switch_tab()  # initialize with first tab
    
    def setup_add_tab(self):
        v = self.v_add
        y = 10
        
        # Type picker (Income / Expense)
        label = ui.Label(frame=(10, y, 130, 30))
        label.text = 'Type (income/expense):'
        label.text_color = 'white'
        v.add_subview(label)
        
        self.t_type = ui.SegmentedControl(frame=(150, y, 200, 30))
        self.t_type.segments = ['income', 'expense']
        self.t_type.selected_index = 1  # default expense
        v.add_subview(self.t_type)
        y += 50
        
        # Category picker as segmented control
        label = ui.Label(frame=(10, y, 130, 30))
        label.text = 'Category:'
        label.text_color = 'white'
        v.add_subview(label)
        
        self.cat_picker = ui.SegmentedControl(frame=(150, y, 200, 30))
        self.cat_picker.segments = ['Food', 'Transport', 'Salary', 'Other']
        self.cat_picker.selected_index = 0
        v.add_subview(self.cat_picker)
        y += 50
        
        # Amount text field
        label = ui.Label(frame=(10, y, 130, 30))
        label.text = 'Amount:'
        label.text_color = 'white'
        v.add_subview(label)
        
        self.t_amt = ui.TextField(frame=(150, y, 200, 30))
        self.t_amt.border_style = ui.TEXT_FIELD_BORDER_STYLE_ROUNDED
        self.t_amt.keyboard_type = ui.KEYBOARD_NUMBERS_AND_PUNCTUATION
        self.t_amt.text_color = 'white'
        self.t_amt.background_color = '#333333'
        v.add_subview(self.t_amt)
        y += 50
        
        # Description text field
        label = ui.Label(frame=(10, y, 130, 30))
        label.text = 'Description (opt):'
        label.text_color = 'white'
        v.add_subview(label)
        
        self.t_desc = ui.TextField(frame=(150, y, 200, 30))
        self.t_desc.border_style = ui.TEXT_FIELD_BORDER_STYLE_ROUNDED
        self.t_desc.text_color = 'white'
        self.t_desc.background_color = '#333333'
        v.add_subview(self.t_desc)
        y += 50
        
        # Add/Update button
        self.btn_add_update = ui.Button(frame=(10, y, 340, 40))
        self.btn_add_update.title = 'Add Entry'
        self.btn_add_update.action = self.do_add_or_update_entry
        v.add_subview(self.btn_add_update)
        
        # Cancel edit button (hidden unless editing)
        self.btn_cancel_edit = ui.Button(frame=(10, y+50, 340, 40))
        self.btn_cancel_edit.title = 'Cancel Edit'
        self.btn_cancel_edit.action = self.cancel_edit
        self.btn_cancel_edit.hidden = True
        v.add_subview(self.btn_cancel_edit)
    
    def do_add_or_update_entry(self, sender):
        """Add new entry or update existing one."""
        etype = self.t_type.segments[self.t_type.selected_index]
        cat = self.cat_picker.segments[self.cat_picker.selected_index]
        amt = self.t_amt.text.strip()
        desc = self.t_desc.text.strip()
        
        # Validation
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
        
        if self.editing_index is None:
            # Add new entry
            save_entry(entry)
            dialogs.alert('Success', 'Entry added!', 'OK')
        else:
            # Update existing entry
            entries = load_entries()
            entries[self.editing_index] = entry
            write_all_entries(entries)
            dialogs.alert('Success', 'Entry updated!', 'OK')
            self.editing_index = None
            self.btn_add_update.title = 'Add Entry'
            self.btn_cancel_edit.hidden = True
        
        self.clear_form()
        self.refresh_list()
    
    def cancel_edit(self, sender):
        self.editing_index = None
        self.clear_form()
        self.btn_add_update.title = 'Add Entry'
        self.btn_cancel_edit.hidden = True
    
    def clear_form(self):
        self.t_type.selected_index = 1  # expense default
        self.cat_picker.selected_index = 0
        self.t_amt.text = ''
        self.t_desc.text = ''
    
    def setup_list_tab(self):
        v = self.v_list
        
        # Table (List view) showing entries
        self.table = ui.TableView(frame=v.bounds.inset(10,10,10,60))
        self.table.data_source = self
        self.table.delegate = self
        self.table.background_color = '#121212'
        self.table.separator_color = '#444444'
        v.add_subview(self.table)
        
        # Delete button
        btn = ui.Button(frame=(10, v.height-50, 340, 40))
        btn.title = 'Delete Selected'
        btn.action = self.do_delete
        v.add_subview(btn)
        self.refresh_list()
    
    def refresh_list(self):
        """Reload entries into the table view sorted by date desc."""
        self.entries = sorted(load_entries(), key=lambda e: e['date'], reverse=True)
        self.selected_row = None
        self.table.reload()
    
    def tableview_number_of_rows(self, tv, section):
        return len(self.entries)
    
    def tableview_cell_for_row(self, tv, section, row):
        cell = ui.TableViewCell()
        e = self.entries[row]
        desc = (e['description'][:20] + '...') if len(e['description']) > 20 else e['description']
        cell.text_label.text = f"{e['date']} | {e['type']} | {e['category']} | ${e['amount']} | {desc}"
        cell.text_label.text_color = 'white'
        cell.background_color = '#121212'
        return cell
    
    def tableview_did_select(self, tv, section, row):
        self.selected_row = row
        # Populate form with selected entry for editing
        entry = self.entries[row]
        self.editing_index = row
        self.segment.selected_index = 0  # Switch to Add Entry tab
        self.switch_tab()
        
        # Set form fields
        self.t_type.selected_index = 0 if entry['type'] == 'income' else 1
        
        # Select category segment or default to 'Other' if missing
        try:
            idx = self.cat_picker.segments.index(entry['category'])
        except ValueError:
            idx = len(self.cat_picker.segments) - 1  # last segment 'Other'
        self.cat_picker.selected_index = idx
        
        self.t_amt.text = entry['amount']
        self.t_desc.text = entry['description']
        
        self.btn_add_update.title = 'Update Entry'
        self.btn_cancel_edit.hidden = False
    
    def do_delete(self, sender):
        """Delete the currently selected entry."""
        if self.selected_row is None:
            dialogs.alert('Warning', 'No entry selected', 'OK')
            return
        
        confirm = dialogs.confirm_alert('Confirm', 'Delete selected entry?', 'Yes', 'No')
        if not confirm:
            return
        
        # Remove from list and rewrite CSV
        entries = load_entries()
        # Find the entry that matches selected_row (list sorted)
        # The displayed entries are sorted by date desc, so use self.entries[self.selected_row]
        entry_to_delete = self.entries[self.selected_row]
        entries = [e for e in entries if e != entry_to_delete]
        
        write_all_entries(entries)
        dialogs.alert('Success', 'Entry deleted', 'OK')
        self.selected_row = None
        self.refresh_list()
    
    def setup_summary_tab(self):
        v = self.v_summary
        self.summary_view = ui.TextView(frame=v.bounds.inset(10,10,10,10))
        self.summary_view.editable = False
        self.summary_view.background_color = '#121212'
        self.summary_view.text_color = 'white'
        v.add_subview(self.summary_view)
    
    def show_summary(self):
        """Compute and display summary stats with category breakdown."""
        entries = load_entries()
        income, expense = 0.0, 0.0
        cat_totals = defaultdict(float)
        for e in entries:
            a = float(e['amount'])
            if e['type'] == 'income':
                income += a
            elif e['type'] == 'expense':
                expense += a
                cat_totals[e['category']] += a
        
        bal = income - expense
        
        txt = (
            f"Total Income: ${income:.2f}\n"
            f"Total Expense: ${expense:.2f}\n"
            f"Current Balance: ${bal:.2f}\n\n"
            "Expenses by Category:\n"
        )
        if cat_totals:
            for cat, amt in cat_totals.items():
                txt += f"  {cat}: ${amt:.2f}\n"
        else:
            txt += "  No expense entries.\n"
        
        self.summary_view.text = txt
    
    def switch_tab(self, sender=None):
        """Show only the active tab view."""
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
        self.main_view.present('sheet')

if __name__ == '__main__':
    TrackerApp().run()
