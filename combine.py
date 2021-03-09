import argparse
import sys

parser = argparse.ArgumentParser(description='Create combination from arguments')
parser.add_argument('--range', metavar='range', type=str, help='range in <from-to> format', action='append')
parser.add_argument('--id', help='print output with row id', default=False, action='store_true')
parser.add_argument('--id-from', metavar='start', help='row id start from', default=1, type=int)

if __name__ == '__main__':
    args = parser.parse_args()

    with_id = args.id
    id_start_from = args.id_from

    # (from, to, offset)
    datasets = []

    # Validate and prepare
    if len(args.__dict__['range']) != 2:
        print('Exact 2 ranges are required, {} given.'.format(len(args.__dict__['range'])))
        sys.exit(1)

    for arg in args.__dict__['range']:
        subargs = arg.split('-')
        subarg1 = ''
        subarg2 = ''
        if len(subargs) == 1:
            subarg1 = subargs[0]
            subarg2 = subargs[0]
        else:
            subarg1 = subargs[0]
            subarg2 = subargs[1]
        if (subarg1.isnumeric() and not subarg2.isnumeric()) or (not subarg1.isnumeric() and subarg2.isnumeric()):
            print('Given range is not consistent: {}'.format(arg))
            sys.exit(1)

        data_range = None
        if (not subarg1.isnumeric() and not subarg2.isnumeric()):
            if len(subarg1) > 1 or len(subarg2) > 1:
                print('String range is unsupported: {}'.format(arg))
                sys.exit(1)
            elif not ( \
                    ord(subarg1) >= ord('A') and ord(subarg1) <= ord('Z') \
                    and ord(subarg2) >= ord('A') and ord(subarg2) <= ord('Z') \
                ) \
                and not ( \
                    ord(subarg1) >= ord('a') and ord(subarg1) <= ord('a') \
                    and ord(subarg2) >= ord('a') and ord(subarg2) <= ord('a') \
                ):
                print('String range is unsupported: {}'.format(arg))
                sys.exit(1)
            else:
                data_range = (0, ord(subarg2) - ord(subarg1), ord(subarg1))
        else:
            data_range = (int(subarg1), int(subarg2), 0)

        if data_range[0] > data_range[1]:
            print('Given range is unsupported (reversed order): {}'.format(arg))
            sys.exit(1)
        
        datasets.append(data_range)

    # Generate
    row_id = 0
    rows = []
    for from_val in range(datasets[0][0], datasets[0][1] + 1):
        for to_val in range(datasets[1][0], datasets[1][1] + 1):
            from_out = from_val
            to_out = to_val
            if datasets[0][2] != 0:
                from_out = chr(from_val + datasets[0][2])
            if datasets[1][2] != 0:
                to_out = chr(to_val + datasets[1][2])
            
            if with_id:
                rows.append('{}, {}, {}'.format(row_id + id_start_from, from_out, to_out))
            else:
                rows.append('{}, {}'.format(from_out, to_out))
            
            row_id = row_id + 1

    # Print
    print("\n".join(rows))