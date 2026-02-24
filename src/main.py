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
    mm, current_time = setup_scenario_1()
    
    # New Invoice Arrives (Immediate Context)
    invoice_123 = MemoryNode("INV_123", "Invoice", "Invoice from Supplier XYZ for ₹2,50,000.", current_time)
    invoice_123.add_edge("SUP_XYZ", "BELONGS_TO")
    mm.add_node(invoice_123)
    
    # The Agent asks the Memory Manager for context related to this invoice
    print(f"Current Interaction: {invoice_123.content}")
    print("Retrieving Relevant Historical Context (Top 3):")
    
    # Query: Agent might ask "quality history" or just retrieve graph distance
    context_results = mm.retrieve_context(invoice_123, current_time, query="quality delay shipment", top_k=3)
    
    for i, (node, score) in enumerate(context_results, 1):
        age = (current_time - node.timestamp).days
        age_str = "Evergreen" if node.is_evergreen else f"{age} days old"
        print(f"  {i}. [Score: {score:.2f}] ({age_str}) - {node.node_type}: {node.content}")

    print("\nDecision Impact:")
    print("> The agent sees the 4-month-old quality issue scored highly due to direct graph proximity (Invoice -> Supplier -> Issue) and severity.")
    print("> The 8-month old payment issue scored lower because of temporal decay (it's older) and lower importance multiplier.")


def setup_scenario_2() -> tuple[MemoryManager, datetime.datetime]:
    """Sets up Example 2: Customer Support Ticket Escalation."""
    mm = MemoryManager()
    current_time = datetime.datetime.now()
    
    # Evergreen Customer Node
    customer_tc = MemoryNode("CUST_TC", "Customer", "TechCorp Inc. (Enterprise)", current_time, is_evergreen=True)
    
    # Historical: Renewed contract 2 months ago (60 days)
    past_date_2m = current_time - datetime.timedelta(days=60)
    renewal_node = MemoryNode(
        "EVENT_01", "Contract", 
        "Customer renewed ₹50 lakh contract. Mentioned considering competitors.", 
        past_date_2m, importance=1.8 # Churn risk is highly important
    )
    
    # Historical: Past similar issue 6 months ago (180 days)
    past_date_6m = current_time - datetime.timedelta(days=180)
    past_issue = MemoryNode(
