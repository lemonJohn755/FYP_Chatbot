# FYP_Chatbot
Telegram chatbot with Rasa

Flow:
1. User say hi to initiate the chatbot to list out available function
2. Select the function (show routes by district/difficulty)
    1. If selects "show routes by district"
        1. Ask user which district
        2. List out the relevant results
    2. If selects "show routes by difficulty"
        1. Ask user difficulty from 1-5
        2. List out the relevant results

Prerequisite:
1. Setup MySQL database to store the sample data of hiking route (download at `sample data` folder)
    - setup MySQL and phpMyAdmin server with `docker-compose.yml` file (type `docker compose up` command in the terminal)
    - database name: FYP_Chatbot
    - table name: sample_data
    - You can insert the sample data from `sample_data\sample_data.sql`
