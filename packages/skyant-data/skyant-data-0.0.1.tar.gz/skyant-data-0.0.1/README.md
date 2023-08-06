
__The package `skyant-data` contains a fleet of tools for working with data in a cloud.__


```python linenums='1' title='installing'
pip3 install skyant-data
```

!!!note
    The `skyant-data` requires __Python>=3.10__


## Philosophy

__SkyANT extends existing objects by implementing additional methods to interact with cloud.__
For example, in popular package [pydantic](https://pydantic-docs.helpmanual.io/) was been added
methods for saving/loading data to/from Google Cloud Storage or Google Firebase (NoSQL database),
send PubSub messages, etc.



## Features

#### data types

- [x] structured (json, yaml)
- [ ] unstructured (jpg, jpeg, png)


#### save/send and load

- [x] to/from Google Cloud Storage
- [x] to/from local file
- [x] to/from Google Firestore
- [x] to Google PubSub topic & Google Tasks
- [ ] to/from REST endpoint (partial completed)


#### other

- [x] send request with an authentication header for Google Cloud Platform (with `skyant-tools`)
- [x] transparently work with a document reference in Google Firestore


<br/>
## [Please read the full documentation on skyant.dev/projects/data](https://skyant.dev/projects/data){ target=_blank}