=====
Usage
=====

To use Python client for dataquality.pl in a project::

    from dq import DQClient


    dq = DQClient('https://app.dataquality.pl', user='<USER_EMAIL>', token='<API_TOKEN>')


API token can be obtain on the page "Moje konto".


Account
=======

Check account status::

    account = dq.account_status()

    print(account.email)          # user email
    print(account.balance)        # account balance
    print(account.total_records)  # processed records


Jobs
====

List jobs
---------
::

    jobs = dq.list_jobs()

    for job in jobs:
        print(job.id)                # job id
        print(job.name)              # human readable job name
        print(job.status)            # job status
        print(job.start_date)        # job start date
        print(job.end_date)          # job end date
        print(job.source_records)    # how many records were applied
        print(job.processed_record)  # how many records were processed
        print(job.price)             # price for processed records


Create new job
--------------
::

    input_data = '''"ID","ADRES"
    6876,"34-404, PYZÓWKA, PODHALAŃSKA 100"
    '''

    job_config = JobConfig('my job')
    job_config.input_format(field_separator=';', text_delimiter='"', has_header=True)
    job_config.input_column(0, name='id', function='PRZEPISZ')
    job_config.input_column(1, name='adres', function='CALY_ADRES')
    job_config.extend(gus=True, geocode=True, diagnostic=True)

    job = dq.submit_job(self, job_config, input_data=input_data)                                         # with data in a variable

    job = dq.submit_job(self, job_config, input_file='my_file.csv', input_file_encoding='windows-1250')  # with data inside file

    print(job.id)
    print(job.name)
    print(job.status)
    ...

Available column functions:

* addresses
    * CALY_ADRES
    * KOD_POCZTOWY
    * MIEJSCOWOSC
    * ULICA_NUMER_DOMU_I_MIESZKANIA
    * NUMER_DOMU_I_MIESZKANIA
    * NUMER_DOMU
    * NUMER_MIESZKANIA
* names
    * NAZWA_OGOLNA
    * NAZWA_PODMIOTU
    * IMIE_I_NAZWISKO
    * IMIE
    * NAZWISKO
* people/companies
    * PESEL
    * NIP
    * REGON
    * EMAIL
* others
    * PRZEPISZ
    * POMIN


Check job state
---------------
::

    state = dq.job_state('3f14e25e-9f6d-41ff-a4cb-942743a37b73')  # input parameter: job id

    print(state)                                                  # 'WAITING' or 'FINISHED'


Cancel job
----------
::

    dq.cancel_job('3f14e25e-9f6d-41ff-a4cb-942743a37b73')  # input parameter: job id


Retrieve job report
-------------------
::

    report = dq.job_report('3f14e25e-9f6d-41ff-a4cb-942743a37b73')  # input parameter: job id

    print(report.quantity_issues)
    print(report.quantity_names)
    print(report.results)


Save job results
----------------
::

    dq.job_results('3f14e25e-9f6d-41ff-a4cb-942743a37b73', 'output.csv')


Delete job and its results
--------------------------
::

    dq.delete_job('3f14e25e-9f6d-41ff-a4cb-942743a37b73')  # input parameter: job id
