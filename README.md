# BG Driving Fines

A very simple script which checks for Bulgarian driving fines and emails on fines.

The sending is done by calling the `sendmail` executable.

You must have the `requests` library installed.

## Usage

```
python3 email_on_driving_fines.py \
    --person-id {BG_citizen_number} \
    --driving-license-id {driving_license_id}
    --mail-to {destination_email}
    --from-mail {from_email_to_provide}

python3 email_on_driving_fines.py -i YYMMDDXXXX -d 123456789 -t destination@example.com -f sender@example.com
```

Keep in mind that invalid combination of ids will result in 404 error from the DMV service.
