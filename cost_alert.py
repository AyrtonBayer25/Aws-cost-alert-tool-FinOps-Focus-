# cost_alert.py
import json
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='AWS Cost Alert Tool - Monitors costs and alerts on thresholds.')
    parser.add_argument('--file', type=str, default=None, help='JSON file path for cost data (default: use mock).')
    parser.add_argument('--threshold', type=float, default=500.0, help='Cost alert threshold (default: 500).')
    return parser.parse_args()

def load_data(file_path):
    if file_path:
        with open(file_path, 'r') as f:
            return json.load(f)
    else:
        mock_data = '''
        {
          "ResultsByTime": [
            {"TimePeriod": {"Start": "2025-11-09"}, "Total": {"UnblendedCost": {"Amount": "650.00"}}},
            {"TimePeriod": {"Start": "2025-11-10"}, "Total": {"UnblendedCost": {"Amount": "400.00"}}}
          ]
        }
        '''
        return json.loads(mock_data)

def check_costs(data, threshold):
    alerts = []
    for result in data.get('ResultsByTime', []):
        try:
            cost = float(result['Total']['UnblendedCost']['Amount'])
            date = result['TimePeriod']['Start']
            if cost > threshold:
                alerts.append(f"ALERT: High cost ${cost} on {date}")
        except KeyError as e:
            print(f"Error processing data: Missing key {e}")
        except ValueError as e:
            print(f"Error converting cost: {e}")
    return alerts

if __name__ == "__main__":
    args = parse_args()
    cost_data = load_data(args.file)  # Renamed 'data' to 'cost_data'
    cost_alerts = check_costs(cost_data, args.threshold)  # Renamed 'alerts' to 'cost_alerts'
    for alert in cost_alerts:
        print(alert)
    if not cost_alerts:
        print("No high costs detected.")