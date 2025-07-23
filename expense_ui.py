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
        # Main container view with multiple subviews
        self.main_view = ui.View(frame=(0, 0, 375, 667))
        self.main_view.name = 'Expense Tracker'
        
        # Top segment controller to switch tabs
        self.segment = ui.SegmentedControl(frame=(10, 30, 355, 30))
        self.segment.segments = ['Add Entry', 'View Entries', 'Summary']
        self.segment.action = self.switch_tab
        self.main_view.add_subview(self.segment)
        
        # Create each tab view
        self.v_add = ui.View(frame=self.main_view.bounds.inset(0, 70, 0, 0))
        self.v_list = ui.View(frame=self.v_add.frame)
        self.v_summary = ui.View(frame=self.v_add.frame)
        
        self.main_view.add_subview(self.v_add)
        self.main_view.add_subview(self.v_list)
        self.main_view.add_subview(self.v_summary)
        
        self.setup_add_tab()
        self.setup_list_tab()
        self.setup_summary_tab()
        
        self.switch_tab()  # initialize with first tab
    
    def setup_add_tab(self):
        v = self.v_add
        # Create input fields and labels for new entry form
        y = 10
        for lbl, name in [('Type (income/expense):', 't_type'),
                          ('Category:', 't_cat'),
                          ('Amount:', 't_amt'),
                          ('Description (opt):', 't_desc')]:
            label = ui.Label(frame=(10, y, 200, 30))
            label.text = lbl
            v.add_subview(label)
            
            tf = ui.TextField(frame=(150, y, 200, 30))
            tf.border_style = ui.TEXT_FIELD_BORDER_STYLE_ROUNDED
            setattr(self, name, tf)
            v.add_subview(tf)
            y += 50
        
        # Submit button
        btn = ui.Button(frame=(10, y, 340, 40))
        btn.title = 'Add Entry'
        btn.action = self.do_add_entry
        v.add_subview(btn)
    
    def do_add_entry(self, sender):
        """Callback when user taps 'Add Entry'."""
        etype = self.t_type.text.strip().lower()
        cat = self.t_cat.text.strip()
        amt = self.t_amt.text.strip()
        desc = self.t_desc.text.strip()
        
        # Basic validation
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
        dialogs.alert('Success', 'Entry added!', 'OK')
        # Clear form
        self.t_type.text = ''
        self.t_cat.text = ''
        self.t_amt.text = ''
        self.t_desc.text = ''
        self.refresh_list()
    
    def setup_list_tab(self):
        v = self.v_list
        # Table (List view) showing entries
        self.table = ui.TableView(frame=v.bounds.inset(10,10,10,60))
        self.table.data_source = self
        self.table.delegate = self
        v.add_subview(self.table)
        
        # Delete button
        btn = ui.Button(frame=(10, v.height-50, 340, 40))
        btn.title = 'Delete Selected'
        btn.action = self.do_delete
        v.add_subview(btn)
        self.refresh_list()
    
    def refresh_list(self):
        """Reload entries into the table view."""
        self.entries = load_entries()
        self.table.reload()
    
    def tableview_number_of_rows(self, tv, section):
        return len(self.entries)
    
    def tableview_cell_for_row(self, tv, section, row):
        # Display each entry in a readable string
        cell = ui.TableViewCell()
        e = self.entries[row]
        cell.text_label.text = f"{e['date']} | {e['type']} | {e['category']} | ${e['amount']} | {e['description']}"
        return cell
    
    def tableview_did_select(self, tv, section, row):
        self.selected_row = row
    
    def do_delete(self, sender):
        """Delete the currently selected entry."""
        if not hasattr(self, 'selected_row'):
            dialogs.alert('Warning', 'No entry selected', 'OK')
            return
        idx = self.selected_row
        confirm = dialogs.confirm_alert('Confirm', 'Delete selected entry?', 'Yes', 'No')
        if not confirm:
            return
        
        # Remove from list and rewrite CSV
        self.entries.pop(idx)
        with open(FILE_PATH, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=HEADERS)
            writer.writeheader()
            writer.writerows(self.entries)
        dialogs.alert('Success', 'Entry deleted', 'OK')
        self.refresh_list()
    
    def setup_summary_tab(self):
        v = self.v_summary
        self.summary_view = ui.TextView(frame=v.bounds.inset(10,10,10,10))
        self.summary_view.editable = False
        v.add_subview(self.summary_view)
    
    def show_summary(self):
        """Compute and display summary stats."""
        entries = load_entries()
        income, expense = 0.0, 0.0
        for e in entries:
            a = float(e['amount'])
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
        self.main_view.present('sheet')
        init_file()

if __name__ == '__main__':
    TrackerApp().run()
