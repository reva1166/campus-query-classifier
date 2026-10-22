"""Hand-written student queries (40 per category, 240 total, all unique).
These are the in-domain data: CLINC150 has no clubs/facilities/academics intents
worth the name, so these queries carry the campus-specific signal."""

QUERIES = {
"academics": """when is the last date to register for the fall semester courses
how do i apply for a grade revaluation
what is the minimum attendance required to sit for exams
who is the professor teaching data structures this semester
where can i find the syllabus for operating systems
when are the end semester exam results going to be published
how many credits do i need to graduate
can i drop a course after the add drop deadline
what is the process to get my transcript
i missed my internal test, can i get a makeup exam
how is the cgpa calculated
when does the project submission window close
is there a way to change my major to electronics
how do i get a bonafide certificate for a scholarship
what are the prerequisites for the machine learning course
where can i see my semester timetable
who is my academic advisor
can i take an elective from another department
what is the passing mark for lab courses
how do i submit my assignment on the lms portal
when is the mid sem exam for calculus
i want to apply for an internship credit
how do i request a re evaluation of my answer sheet
what is the deadline to submit the thesis
are there any tutorials for linear algebra this week
how can i get the previous year question papers
whats the grading scheme for chemistry
my attendance is showing wrong on the portal who do i contact
can i do a minor in business studies
when will the hall tickets be released
how do i apply for the dual degree program
which books are recommended for thermodynamics
what time is the physics lecture on monday
is there a course on deep learning for undergraduates
how do i withdraw from the semester
i need help with my research paper citations
who do i talk to about a course waiver
when is the convocation registration
do i get extra time in exams because of my disability
what are the office hours of the maths professor""".split("\n"),

"events": """what events are happening on campus this weekend
when is the annual tech fest
how do i register for the hackathon
is there a cultural night this friday
where will the freshers party be held
who is performing at the college fest
are tickets required for the football match
when does the sports day start
is there a guest lecture tomorrow evening
how can i volunteer for the orientation program
what time does the convocation ceremony begin
is there any workshop on resume building this week
when is the diwali celebration on campus
can i bring a friend to the music concert
where can i find the schedule of the inter college competition
is the alumni meet open for all students
what is the theme of this year's cultural festival
are there any career fair events next month
when is the dance competition
is the open mic night still happening
how do i buy passes for the fest
is the movie screening tonight free
when do registrations close for the quiz competition
what's on at the auditorium on saturday
is there a seminar on entrepreneurship
can you list upcoming events for this month
who is the chief guest at the annual day
where is the startup pitch event taking place
is there a marathon organized by the college
what time does the fashion show start
will there be fireworks at the fest
how do i get a volunteer pass for the techno cultural event
is the independence day program open to everyone
when is the poetry slam
is there a blood donation camp this week
are food stalls going to be there at the fest
what events are there for first year students
where can i see the event poster
is there a talent show this semester
when is the farewell party for seniors""".split("\n"),

"transport": """when does the next college bus leave
what is the bus route from the hostel to main gate
where can i park my bike on campus
is there a shuttle to the metro station
how do i get a bus pass
what time is the last bus to the city
is there a cab service from campus to the airport
how much does the monthly bus pass cost
which bus goes to the railway station
is the shuttle running on sundays
can i get a parking permit for my car
where is the nearest bus stop
how long does it take to reach the college from the city center
do you have a bus tracking app
is there an electric cart for moving around campus
what is the bus timing from the north gate
can i bring my bicycle on the college bus
how do i change my bus route
is the evening shuttle delayed today
where can i book an auto rickshaw near the campus
are there any buses to the nearest mall on weekends
what is the fare for the staff shuttle
where does the hostel bus pick up from
can guests use the campus shuttle
is there a carpool group for students
how far is the nearest metro station
do buses run during exam holidays
where is the bus pickup point for the south campus
how do i report my lost bus pass
is two wheeler parking free for students
is there a bike sharing service on campus
what time does the first bus leave in the morning
can i get a refund for my unused bus pass
which route does bus number 12 take
is there a late night transport for the library users
how do i get to the college from the airport
are there ev charging points in the parking lot
who is the transport in charge
is there an overnight bus for students going home on holidays
what are the rules for bringing a car to campus""".split("\n"),

"clubs": """how do i join the coding club
when are the auditions for the drama society
who is the president of the photography club
what clubs are available for first year students
how can i start a new student club
when is the next robotics club meeting
is there a debate club on campus
how do i sign up for the music society
what does the entrepreneurship cell do
are recruitments open for the literary club
how much is the membership fee for the chess club
where does the dance club practice
can i be a member of more than one club
who do i contact to join the nss
when does the ncc enrollment start
is there a gaming club here
what are the club recruitment dates
how do i apply for a core team position in the design club
does the college have a cycling club
where do the astronomy club members meet
how many clubs can i join
when is the club fair
how do i get funding for my club activity
is there an environment club that does tree plantation
can seniors also join the quiz club
who is the faculty advisor of the film club
what is the selection process for the editorial board
how do i contact the student council
is the volunteering club taking new members
do i need prior experience to join the ai club
what is the schedule of the yoga club sessions
can i switch from one club to another
are there any clubs related to finance
how do i leave a club
where is the club notice board
does the mountaineering club organize treks
when does the open house for clubs take place
how do i become a coordinator of the cultural club
is the toastmasters club active in our college
where can i find a list of all registered student societies""".split("\n"),

"facilities": """what are the library opening hours
is the gym open on sundays
where is the nearest atm on campus
how do i book a study room in the library
what is the wifi password for the hostel
where can i get my id card printed
is the swimming pool open in the evening
what time does the canteen close
how do i report a broken fan in my room
where is the health center located
is a doctor available at the medical centre at night
what facilities are there in the sports complex
can i book the badminton court
where are the printing and xerox shops
how do i get a locker in the library
is the laundry service available in the hostel
what is on the mess menu today
where is the computer lab
the water cooler on the second floor is not working
how can i reserve a seminar hall
where can i find a quiet place to study
what are the visiting hours for the hostel
does the campus have a pharmacy
how do i apply for a hostel room
is there a cafeteria near the engineering block
where is the post office on campus
the wifi in my block is very slow who do i complain to
can i borrow a laptop from the library
what is the mess timing for dinner
how do i get access to the 3d printing lab
how many books can i issue from the library at once
where can i get a bank account opened on campus
is there a barber shop in the campus
how do i request maintenance for the air conditioner
are there any vending machines around
what are the timings of the stationery shop
where is the counselling centre
can i use the football ground in the evening
is the library open during exams till late
how do i get a new hostel room key""".split("\n"),

"other": """what is the weather like today
tell me a joke
who won the cricket match yesterday
how do i cook pasta
what is the capital of australia
play some relaxing music
what is the meaning of life
how much is a flight ticket to london
can you recommend a good movie
what is the price of bitcoin
how are you doing today
what is the best pizza place in new york
how do i fix a leaking tap at home
who is the prime minister of japan
set an alarm for six am
what's the stock price of apple
how many calories are in a banana
tell me something interesting
i want to book a hotel in goa
how do i change a flat tire
what is your name
what is the score of the football game
how old is the universe
can you flip a coin
what's the exchange rate for dollars to rupees
recommend a good book to read for fun
how do i lose weight fast
who invented the telephone
is it going to rain tomorrow
order me a large pepperoni pizza
what time is it in tokyo
do you like movies
how do i file my income tax returns
what is a good gift for my mother
how tall is mount everest
can you sing a song
what's the best smartphone under 20000
how do i get my credit card limit increased
what are the symptoms of the common cold
call my mom""".split("\n"),
}
