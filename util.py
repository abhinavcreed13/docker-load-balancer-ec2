import argparse

def get_args():
    """Argument parser.

    Returns:
      Dictionary of arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--url',
        type=str,
        help='URL to be called')
    parser.add_argument(
        '--time-dist',
        type=str,
        choices=['normal','poisson'],
        help='Inter-Request time distribution')
    parser.add_argument(
        '--mu',
        type=float,
        help='Mean for Normal distribution')
    parser.add_argument(
        '--sigma',
        type=float,
        help='standard deviation for normal distribution')
    parser.add_argument(
        '--lamb',
        type=float,
        help='lambda for poisson distribution')
    parser.add_argument(
        '--iter',
        type=int,
        help='Number of iterations of URL calls to be done before the program terminates')
    parser.add_argument(
        '--database',
        type=str,
        help='Name of the database')
    parser.add_argument(
        '--api-url',
        type=str,
        default="http://localhost:70/api/v1.3/subcontainers/docker/",
        help='Docker API URL')
    parser.add_argument(
        '--mongo-client',
        type=str,
        default="localhost",
        help='Mongo DB source client')
    parser.add_argument(
        '--simulate-load',
        type=str,
        default="True",
        help='Mongo DB source client')
    parser.add_argument(
        '--write-to-file',
        type=str,
        default="True",
        help='Write collections to file')
    parser.add_argument(
        '--replicate',
        type=int,
        default=2,
        help='Replication of application')
    parser.add_argument(
        '--mode',
        type=str,
        choices=['deploy','display','leave'],
        help='mode for the script')
    parser.add_argument(
            '--init-swarm',
            type=str,
            default="True",
            help='init swarm')
    parser.add_argument(
            '--mount-mongo',
            type=str,
            help='mongo db mount path')
    args, _ = parser.parse_known_args()
    return args