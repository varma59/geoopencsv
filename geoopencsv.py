import csv
import os
import geoip2.database

GEOIP_DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'GeoLite2-Country.mmdb')

def geoopencsv(input_csv_file, output_csv_file):
    try:
        with open(GEOIP_DATABASE_PATH, 'rb'):
            pass
    except FileNotFoundError:
        print("GeoLite2-Country.mmdb database file not found in the project directory.")
        return

    try:
        reader = geoip2.database.Reader(GEOIP_DATABASE_PATH)
    except Exception as e:
        print(f"Error: {e}")
        return

    with open(input_csv_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        
        with open(output_csv_file, 'w', newline='') as output_file:
            csv_writer = csv.writer(output_file)
            
            for row in csv_reader:
                ip_address = row[0].split(':')[0] 
                port_number = row[0].split(':')[1] if len(row[0].split(':')) > 1 else '' 
                
                try:
                    response = reader.country(ip_address)
                    country_name = response.country.name
                    csv_writer.writerow([ip_address, port_number, country_name])
                except geoip2.errors.AddressNotFoundError:
                    csv_writer.writerow([ip_address, port_number, 'Unknown'])
                except Exception as e:
                    print(f"Error processing IP {ip_address}: {e}")
