
from synthetic_generator import (
    generate_person_parts,
    generate_address,
    generate_object_name,
    generate_customer_name,
)

print("ФИО:")
print(generate_person_parts("TEST_PERSON_1"))
print(generate_person_parts("TEST_PERSON_1"))

print("\nАдрес:")
print(generate_address("TEST_ADDRESS_1"))

print("\nТехническое название:")
print(generate_object_name("Старая подстанция", "TEST_OBJECT_1", "Substation"))

print("\nНазвание абонента:")
print(generate_customer_name("Старый абонент", "TEST_CUSTOMER_1"))
