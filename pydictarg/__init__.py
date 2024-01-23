# usage
# import pydictarg
# pydictarg.args_to_dict(sys.argv)
import sys

def args_to_dict(argv):
    args = {}
    args_i = 0
    i = 0
    while i < len(argv):
        if argv[i][:1] == '-':
        # if the current argument starts with a dash
            if (i+1 >= len(argv)) or (argv[i+1][:1] == '-'):
            # if last argument or folowed by dash
                # leave present but empty
                args[argv[i]] = ''
            else:
            # if last argument or folowed by dash
                args[argv[i]] = argv[i+1]
                i += 1
        else:
        # does not start with dash
            # add to as next available integer key
            args[args_i] = argv[i]
            args_i += 1
        i += 1
    
    return args

if __name__ == '__main__':
	print(args_to_dict(sys.argv))
