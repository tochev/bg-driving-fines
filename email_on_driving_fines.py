#!/usr/bin/env python3
import argparse
import subprocess
import textwrap
import typing

import requests


NO_OBLIGATIONS_RESPONSE = {
    "obligationsData": [
        {
            "unitGroup": 1,
            "errorNoDataFound": False,
            "errorReadingData": False,
            "obligations": []
        },
        {
            "unitGroup": 2,
            "errorNoDataFound": False,
            "errorReadingData": False,
            "obligations": []
        }
    ]
}


def get_fines_info(person_id: str, driving_license_id: str, return_error_as_text=True) -> typing.Union[bool, str]:
    """
    Return fines information or text indicating an error, `False` on no fines.
    """
    response = requests.get(
        'https://e-uslugi.mvr.bg/api/Obligations/AND',
        params=dict(
            obligatedPersonType=1,  # physical person
            additinalDataForObligatedPersonType=1,  # driving license
            mode=1,
            obligedPersonIdent=person_id,
            drivingLicenceNumber=driving_license_id,
        )
    )
    try:
        response.raise_for_status()
        if response.json() != NO_OBLIGATIONS_RESPONSE:
            return response.text
        else:
            return False
    except Exception as e:
        if return_error_as_text:
            return repr(e)
        else:
            raise


def mail_on_fines(person_id: str, driving_license_id: str, mail_to: str, from_mail: str):
    info = get_fines_info(person_id=person_id, driving_license_id=driving_license_id)
    if info is False:
        pass
    else:
        mail = textwrap.dedent(
            f'''\
            From: {from_mail}
            To: {from_mail}
            Subject: Driving fines {str(person_id)[:6]}

            Returned info:
               {info}
            '''
        )
        subprocess.run(['sendmail', mail_to], input=mail.encode('utf-8'), check=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check for BG driving fines and email on fines')
    parser.add_argument('-i', '--person-id', required=True, help='BG citizen number')
    parser.add_argument('-d', '--driving-license-id', required=True, help='driving license id')
    parser.add_argument('-t', '--mail-to', required=True, help='send to mail')
    parser.add_argument('-f', '--from-mail', required=True, help='send to mail')

    args = parser.parse_args()

    mail_on_fines(
        person_id=args.person_id, driving_license_id=args.driving_license_id,
        mail_to=args.mail_to, from_mail=args.from_mail,
    )
