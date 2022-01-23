from greedy import Greedy
from hillClimbing0 import HillClimbing
import sys


# h0 = HillClimbing('test.txt','outTest.txt')
# h0.writeSolutions()

# h1 = HillClimbing('arq_input_aes.txt','outAesHill.txt')
# h1.writeSolutions()

# h2 = HillClimbing('arq_input_gsm.txt','outGsmHill.txt')
# h2.writeSolutions()

# h3 = HillClimbing('arq_input_sha.txt','outShaHill.txt')
# h3.writeSolutions()

# h4 = Greedy('arq_input_sha.txt','outShaGreedy.txt')
# h4.writeSolutions()

if __name__ == "__main__":
    benchmark = sys.argv[1]
    output = sys.argv[2]
    result = HillClimbing(benchmark,output)
    result.writeSolutions()