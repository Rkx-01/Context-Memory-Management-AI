import datetime
from memory_system import MemoryManager, MemoryNode

def print_separator(title=""):
    print(f"\n{'='*20} {title} {'='*20}")

def setup_scenario_1() -> tuple[MemoryManager, datetime.datetime]:
    """Sets up Example 1: Invoice Processing with Historical Context."""
    mm = MemoryManager()
    current_time = datetime.datetime.now()
    
    # Create Supplier Node (Evergreen)
    supplier_xyz = MemoryNode("SUP_XYZ", "Supplier", "Supplier XYZ", current_time, is_evergreen=True)
    
    # Create Historical Context (4 months ago, roughly 120 days)
    past_date_4m = current_time - datetime.timedelta(days=120)
    issue_1 = MemoryNode(
        "ISSUE_01", "Issue", 
        "Delivered 30% broken products, leading to ₹50,000 replacement costs and 2-week delay.", 
        past_date_4m, importance=1.5 # High importance
    )
    
    # Create Historical Context (8 months ago -> 240 days)
    past_date_8m = current_time - datetime.timedelta(days=240)
    payment_issue = MemoryNode(
        "ISSUE_02", "Payment_Issue", 
        "Disputed an invoice claiming non-receipt despite early payment discount.", 
        past_date_8m
    )
    
    # Create Seasonal Context (Summer months)
    seasonal_pattern = MemoryNode(
        "PATTERN_01", "Pattern", 
        "Delivery quality degrades during summer months (March-May) due to heat-sensitive packaging.", 
        current_time, is_evergreen=True # This is an evergreen rule/fact, not a single decayable event
    )
    
    # Add to manager
    for node in [supplier_xyz, issue_1, payment_issue, seasonal_pattern]:
        mm.add_node(node)
        
    # Build Graph Relationships
    mm.link_nodes("SUP_XYZ", "ISSUE_01", "EXPERIENCED_QUALITY_ISSUE")
    mm.link_nodes("SUP_XYZ", "ISSUE_02", "EXPERIENCED_PAYMENT_ISSUE")
    mm.link_nodes("SUP_XYZ", "PATTERN_01", "EXHIBITS_PATTERN")
    
    return mm, current_time

def run_scenario_1():
    print_separator("Scenario 1: Invoice Processing")
