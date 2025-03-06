from django.utils.translation import gettext as _
import numpy as np

def generate_error_return(instance_name_str, checksum_return=False):
    from insuree.apps import InsureeConfig
    if checksum_return:
        return [{"errorCode": InsureeConfig.validation_code_invalid_insuree_number_checksum,
                 "message": _(f"{instance_name_str}_national_id_checksum_not_valid")}]
    else:
        return [{"errorCode": InsureeConfig.validation_code_invalid_insuree_number_exception,
                 "message": _(f"{instance_name_str}_national_id_not_valid")}]


ZERO_CHAR = '0'
NINE_CHAR = '9'


class IdentifierValidator:
    """
    A class for validating Moldovan national identification numbers (IDs).
    Can be specified as an insuree number validator in apps.py config with the key: "insuree_number_validator"
    Example: "insuree_number_validator": IdentifierValidator().is_valid_resident_identifier
    """

    @staticmethod
    def is_valid(idn):
        if idn is None or len(idn) != 13 or not idn.strip():
            return False
        crc = 0
        for i in range(12):
            if not (ZERO_CHAR <= idn[i] <= NINE_CHAR):
                return False
            crc += (ord(idn[i]) - ord(ZERO_CHAR)) * (7 if i % 3 == 0 else (3 if i % 3 == 1 else 1))
        if not (ZERO_CHAR <= idn[12] <= NINE_CHAR):
            return False
        return crc % 10 == (ord(idn[12]) - ord(ZERO_CHAR))

    @staticmethod
    def is_valid_resident_identifier(idnp):
        if not IdentifierValidator.is_valid(idnp):
            return generate_error_return("resident")
        if not (idnp[0] == '2' or idnp.startswith('09')):
            return generate_error_return("resident", checksum_return=True)

    @staticmethod
    def is_valid_organization_identifier(idno):
        if not IdentifierValidator.is_valid(idno):
            return generate_error_return("organization")
        if not idno[0] == '1':
            return generate_error_return("organization", checksum_return=True)

    @staticmethod
    def is_valid_vehicle_identifier(idnv):
        if not IdentifierValidator.is_valid(idnv):
            return generate_error_return("vehicle")
        if not idnv[0] == '3':
            return generate_error_return("vehicle", checksum_return=True)

##AUTOGENERATE CHFID

def generate_incremental_chfid():
    from .models import TblInsuree

    # Get all CHFIDs that start with 'S' and are followed by digits only
    insurees_with_valid_chfid = TblInsuree.objects.filter(chfid__regex=r'^S\d{8}$').order_by('chfid')

    if insurees_with_valid_chfid.exists():
        last_insuree = insurees_with_valid_chfid.last()
        last_chfid = last_insuree.chfid[1:]  # Remove the prefix 'S'
        
        # Check if the last_chfid is a valid integer
        if last_chfid.isdigit():
            new_chfid = 'S' + str(int(last_chfid) + np.random.randint(1,50)).zfill(8)  # Increment and add leading zeros
        else:
            new_chfid = 'S00000001'  # Default starting value
    else:
        new_chfid = 'S00000001'  # Starting point if no valid records exist

    return new_chfid
