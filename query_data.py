from sqlalchemy import extract
from sqlalchemy.orm import Session
import numpy
from create import *

session = Session(bind=engine)

def show_top_offices(year, month):
    offices=session.query(Office).all()
    sale_count=[0]*(len(offices)+1)
    
    #Queries the sales in the desired period
    sales=session.query(Sale).filter(
        extract('year', Sale.sale_date)==year,
        extract('month', Sale.sale_date)==month).all()
    
    #Checks which office was responsible for each listing, and update the count accordingly
    for sale in sales:
        sale_count[sale.listing.office_id]+=1
    
    #In the count array, the index correspond to office ids
    #So ordering the indexes using numpy will order the offices by most sales
    #It gives them in ascending order, so we invert it to get descending order
    office_order=numpy.argsort(sale_count)[::-1]
    
    print("Best selling offices:")
    for i, office_id in enumerate(office_order[0:5]):
        try:
            office=session.query(Office).filter(Office.id==int(office_id)).one()
            print(f"#{i+1} - {office.name} with {sale_count[office_id]} sales")
        except:
            print(office_id)
            pass

def show_top_agents(year, month):
    agents=session.query(Agent).all()
    for agent in agents:
        sales=session.query(Sale).filter(
            Sale.sale_agent == agent,
            extract('year', Sale.sale_date)==year,
            extract('month', Sale.sale_date)==month).all()
        agent.sales_count=len(sales)
    
    #Sort agents based on the sales_count, descending
    agents.sort(key=lambda agent: agent.sales_count, reverse=True)

    print("Best selling agents:")
    for i, agent in enumerate(agents[0:5]):
        print(f"#{i+1} - {agent.name}, with {agent.sales_count} sales, available at {agent.email}")
        

def show_sales_data(year, month):
    sales=session.query(Sale).filter(
        extract('year', Sale.sale_date)==year,
        extract('month', Sale.sale_date)==month).all()

    total_time = 0
    total_price = 0

    for sale in sales:
        time_market = (sale.sale_date - sale.listing.list_date).days
        total_time += time_market
        total_price += sale.sale_price

    avg_time=total_time/len(sales)
    avg_price=total_price/len(sales)

    print(f"The average price was ${avg_price:.2f} and average time in the market was {avg_time:.2f} days")

def save_monthly_comissions(year,month):
    #Prevents adding the same month twice to the comissions table
    comissions = session.query(MonthlyComission).filter(MonthlyComission.month==month, MonthlyComission.year==year).all()
    if len(comissions)>0:
        print("Comissions already added for this month")
        return 0
    
    agents=session.query(Agent).all()
    for agent in agents:
        sales=session.query(Sale).filter(
            Sale.sale_agent == agent,
            extract('year', Sale.sale_date)==year,
            extract('month', Sale.sale_date)==month).all()
        agent.total_comission=0
        for sale in sales:
            agent.total_comission+=sale.sale_comission
        session.add(MonthlyComission(agent_id=agent.id, total_comission=agent.total_comission, month=month, year=year))
        print(f"{agent.name} earned {agent.total_comission} this month")
    session.commit()

def get_monthly_report(year, month):
    print(f"################### REPORTS FOR {month}/{year} ##########################")
    show_top_offices(year, month)
    show_top_agents(year, month)
    show_sales_data(year, month)
    save_monthly_comissions(year, month)

def get_monthly_reports():
    get_monthly_report(2022, 1)
    get_monthly_report(2022, 2)
    get_monthly_report(2022, 3)

get_monthly_reports()