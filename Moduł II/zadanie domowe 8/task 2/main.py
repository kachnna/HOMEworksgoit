from producer import producer_run
from consumer import consume_messages
import connect


if __name__ == "__main__":
    producer_run()
    consume_messages()
