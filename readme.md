## **TicketVendor**

This Rest api will manages all the tickets for the shows, movies and concerts. This API is built on the top of the django rest framework.

#### Note : -
There is not mention of add seat in a database. So i had implemented another endpoint. So refer the 4 endpoint list below. First add a single Seat then proceed with other endpoint.

#### Steps to run the django app:-

1. Create a virtual env with `python3 -m venv env`
2. Activate virtual env with `. env/bin/activate`
3. Install requirements using `pip install -r requirements.txt`
4. Run the server locally using `python3 manage.py runserver`
5. Go to `http://127.0.0.1:8000/`

#### **Endpoints**
1. /api/vacate : This endpoint takes the person name and the seat number to vacate that particular seat. Make a post request to this endpoint with content type="application/json"
<br> Example :-
<br> Endpoint `http://127.0.0.1:8000/api/vacate/ `
<br> Data
`{
 "SEATNUM":"A1"
}`

2. /api/get_info/[ticket_id or Person name or Seat no] : This endpoint will provide you all the information about your ticket.
Simple add the ticket_id or Person name or Seat no in the url and it will give a response in json format.
<br> Example : - Direct url `http://127.0.0.1:8000/api/get_info/A1`

3. api/occupy : This endpoint will search all the seat. If it finds one then it will book  that for you and provide details in response but if it unable to find one then it will raise 404 status code with All seats reserved.
<br> Example : -
<br> Endpoint  `http://127.0.0.1:8000/api/occupy`
<br> Data `{
        "ticket_id": "2edc7cc5-f436-4104-b799-64ca94cd3e2e",
        "person_name": "Praveen Chaudhary"
}`

4. /api/add_seat : This endpoint will add seat to the database and checks that the number of seat will not exceed the MAX_OCCUPANCY 
<br> Example : -
<br> Endpoint `http://127.0.0.1:8000/api/add_seat`
<br> Data `{
    "SEATNUM": "A2"
}`

