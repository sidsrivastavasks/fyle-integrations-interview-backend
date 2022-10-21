# Fyle Integrations Backend Challenge

## Who is this for?

This challenge is meant for candidates who wish to work / intern at Fyle and work with our engineering teams.

If it is for internship, you should be able to commit to at least 6 months.

## Why work at Fyle?

Fyle is a fast-growing Expense Management SaaS product. We are ~40 strong engineering team at the moment.

We are an extremely transparent organization. Check out our [careers page](https://careers.fylehq.com) that will give you a glimpse of what it is like to work at Fyle. Also, check out our Glassdoor reviews [here](https://www.glassdoor.co.in/Reviews/Fyle-Reviews-E1723235.htm). You can read stories from our teammates [here](https://stories.fylehq.com).

## Challenge outline

This is a web application designed in a context of a single classroom.
Described [here](./Application.md)

### My tasks

1. Add missing APIs mentioned [here](./Application.md#Missing-APIs)
2. Get the automated tests to pass
3. Get the test coverage to 90% or above
4. Feel free to add more test cases, try to increase the coverage as much as you can

## Installation

1. Fork this repository to your github account
2. Clone the forked repository and proceed with steps mentioned below

### Install requirements

```
virtualenv env --python=python3.8
source env/bin/activate
pip install -r requirements.txt
```

### Reset DB

```
rm db.sqlite3
```

### Reset Test DB

```
rm test_db.sqlite3
```

### Start Server

```
bash run.sh
```

### Run Tests

```
pytest tests/ --cov
```

## Available API's for Teachers

### Auth

-   header: "X-Principal"
-   value: {"user_id":2, "teacher_id":2}

For APIs to work we need a principal header to establish identity and context

### GET /teacher/assignments

#### List all assignments submitted to this teacher

```
headers:
X-Principal: {"user_id":2, "teacher_id":2}

response:
{
    "data": [
        {
            "content": "ESSAY T1",
            "created_at": "2021-09-17T03:14:01.580126",
            "grade": null,
            "id": 1,
            "state": "SUBMITTED",
            "student_id": 1,
            "teacher_id": 1,
            "updated_at": "2021-09-17T03:14:01.584644"
        }
    ]
}
```

### PATCH /teacher/assignments/

#### Grade an assignment

```
headers:
X-Principal: {"user_id":3, "teacher_id":1}

payload:
{
    "id":  1,
    "grade": "A"
}

response:
{
    "data": {
        "content": "ESSAY T1",
        "created_at": "2021-09-17T03:14:01.580126",
        "grade": "A",
        "id": 1,
        "state": "GRADED",
        "student_id": 1,
        "teacher_id": 1,
        "updated_at": "2021-09-17T03:20:42.896947"
    }
}
```

---

# New Test

## Student Test

<br>

#### PATCH test_set_state_assignment_student_1

```
It will try to set the Grade from Student account
```

<br>

#### PATCH test_grade_assignment_student_1

```
It will test wheather student can give grade to an assignment
```

## Teacher Test

<br>

#### PATCH test_wrong_assignment_id

```
Test with an Assignment which is not present in the Database
```

---
