# E-commerce-Admin-API
Setup:

Create a virtual environment:

  python3 -m venv env
  source env/bin/activate

Install Requirements:

  pip3 install -r requirements.txt

To run the server:

  uvicorn main:app --reload

To populate the database with demo data:

  python3 seed_data.py


Endpoints:

Sales Status:

 Get Sales:
    Get: 
      /sales
 Get Daily Revenue:
    Get:
      /revenue/daily
 Revenue Comparison:
    Get:  
      /revenue/comparison

Inventory Management:

  View current inventory status and low stock alerts:
    Get:
      /inventory/

  Update Inventory:

    Put:
      /inventory/{product_id}

  Track Inventory and changes:

    Get:
     /inventory/track/{product_id} 
    
