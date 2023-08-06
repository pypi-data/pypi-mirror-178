def mathValidation(validation):
    count = len(validation) + 1
    sum = 0
    for number in range (len(validation)):
        sum += int(validation[number]) * count
        count -= 1
    return sum


def verifyCPF(sum, cpf, validation):
    verify = sum % 11
    if verify < 2:
        verify = 0
    else:
        verify = 11 - verify
    if verify == int(cpf[len(validation)]):
        return True, verify
    else:
        return False, 0

def validateCPF(cpflist):
    """Analizes if the last 2 digits of the received CPF validates the entire string.
    
    Parameter:
        cpf (str): The string which will be verified
        
    Return:
        validation (bool): Default value for validation is False
    """
    validated = False
    #Applying first step of validation
    cpf = [int(char) for char in cpflist if char.isdigit()]

    if len(cpf) == 11 and cpf != cpf[::-1]:
        #Applying second step of validation.
        validation = cpf[:9]
        sum = mathValidation(validation)
        boolVerification, verify = verifyCPF(sum, cpf, validation)

        #Applying third step of validation
        if boolVerification:
            validation.append(verify)
            sum = mathValidation(validation)
            boolVerification, verify = verifyCPF(sum, cpf, validation)
            if boolVerification:
                validated = True
    return validated

