import os

def get_input(prompt, valid_options=None):
    """Get user input with validation."""
    while True:
        value = input(prompt).strip()
        if valid_options is not None and value not in valid_options:
            print(f"Error: opción inválida. Las opciones válidas son: {', '.join(valid_options)}")
        else:
            return value

file_path = get_input("Ingresa la ruta del archivo: ")

region = get_input("Ingresa la región deseada: ")
ami = get_input("Ingresa la AMI: ")
vpc_id = get_input("Ingresa el ID del VPC: ")
subnet_id = get_input("Ingresa el ID de la subred: ")
instance_type = get_input("Ingresa el tipo de instancia: ")

template = f"""provider "aws" {{
  region = "{region}"
}}

resource "aws_vpc" "example" {{
  id = "{vpc_id}"
}}

resource "aws_subnet" "example" {{
  vpc_id = aws_vpc.example.id
  cidr_block = "{subnet_id}"
}}

resource "aws_instance" "example" {{
  ami           = "{ami}"
  instance_type = "{instance_type}"
  subnet_id     = aws_subnet.example.id
}}"""

with open(file_path, "w") as f:
    f.write(template)

print("Archivo Terraform creado exitosamente en:", file_path)
