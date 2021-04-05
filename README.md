# Similarity

Plagiarism checker RESTful API using NLP.

## Functionality

Users register with credentials and are given a fixed amount of tokens. Tokens are required
to request information. Users are then able to detect similarity between two documents
based on a pre-trained model. 

Credentials are hashed and salted before storing in MongoDB.

### Example

```
Request: 
(/detect)
{
    "Username": "John Doe",
    "Password": "xxx",
    "Text_1": "The quick brown fox jumped over the lazy dog.",
    "Text_2": "The dog is lazy but the brown fox is quick!"
}

Response:
{
    "Status": 200,
    "Similarity": 0.5619030005377265,
    "Message": "Similarity score calculated successfully"
}
```

## Resource

|Resource            | Address   | Protocol  | Parameters               | Response/Status                                                                           |
| ------------------ | --------- | --------- | ------------------------ | ------------------------------------------------------------------------------------------|
| Register User      | /register | POST      | Username, Password       | 200 OK <br />401 Invalid Username                                                         |
| Detect Similarity  | /detect   | POST      | Username, Password, Note | 200 OK <br />401 Invalid Username <br />402 Incorrect Password <br />403 Not Enough Tokens|
| Refill Tokens      | /refill   | POST      | Username, Password       | 200 OK <br />401 Invalid Username <br />404 Incorrect Admin Password                      |

### Token System
- Each user gets 10 tokens upon registering.
- Tokens are required to store and fetch notes.
- Buy more tokens when user runs out.