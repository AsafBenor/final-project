import time
import multiprocessing as mp
import csv
from graph import Graph, Node  # Assumes you already have these classes implemented

# Timeout in seconds (1 hour = 3600 seconds)
TIMEOUT = 3600
POLL_INTERVAL = 1  # seconds between timeout checks
OUTPUT_TEXT_FILENAME = "results.txt"
OUTPUT_CSV_FILENAME = "results_excel.csv"


def compute_winning_states_for_board(board_size, queue):
    """
    Creates a board and graph for the given board_size.
    Computes the winning states and puts the results (board size, elapsed time,
    and number of winning states) into the provided queue.
    """
    # Generate board of size n x n with only open cells ('-')
    board = ["-" * board_size for _ in range(board_size)]

    # Create the graph from the board
    graph = Graph()
    graph.create_graph(board)

    # Measure the time to compute winning states
    start_time = time.time()
    winning_states, winning_state_parents = graph.find_winning_states()
    elapsed_time = time.time() - start_time

    # Send results (board_size, elapsed_time, number of winning states) to the parent process
    queue.put((board_size, elapsed_time, len(winning_states)))


def main():
    board_size = 3  # starting board size (3x3)
    results = []  # List to store tuples: (board_size, elapsed_time, num_winning_states, status)

    print("Starting computation of winning states with increasing board sizes...\n")
    while True:
        print(f"Processing board size: {board_size}x{board_size}...", flush=True)
        queue = mp.Queue()
        process = mp.Process(target=compute_winning_states_for_board, args=(board_size, queue))
        process.start()

        # Enforce a hard timeout by checking the elapsed wall-clock time
        start_wait = time.time()
        while process.is_alive():
            time.sleep(POLL_INTERVAL)
            elapsed_wait = time.time() - start_wait
            if elapsed_wait > TIMEOUT:
                print(f"Board size {board_size}x{board_size} TIMED OUT after {TIMEOUT} seconds.")
                process.terminate()
                process.join()
                results.append((board_size, None, None, "TIMED OUT"))
                break
        else:
            # This else block executes if the while loop wasn't broken (i.e., process finished in time)
            try:
                size, elapsed, num_winning = queue.get_nowait()
                results.append((size, elapsed, num_winning, "OK"))
                print(f"Completed board size {size}x{size}: Time = {elapsed:.2f} sec, Winning states = {num_winning}")
            except Exception as e:
                error_msg = f"ERROR: {e}"
                results.append((board_size, None, None, error_msg))
                print(f"Error on board size {board_size}x{board_size}: {error_msg}")

        # If the result for this board was a timeout, stop testing further
        if results[-1][3] != "OK":
            break

        board_size += 1
        print("-" * 50)

    # Write the text summary file (results.txt)
    try:
        with open(OUTPUT_TEXT_FILENAME, "w") as f:
            f.write("Graph Winning States Computation Results\n")
            f.write("========================================\n")
            f.write(f"Timeout per board: {TIMEOUT} seconds (1 hour)\n\n")
            f.write("{:<10} {:<25} {:<25}\n".format("Board", "Time (sec)", "Winning States"))
            f.write("-" * 60 + "\n")

            for board, elapsed, num_winning, status in results:
                board_label = f"{board}x{board}"
                if status != "OK":
                    line = "{:<10} {:<25} {:<25}\n".format(board_label, status, "N/A")
                else:
                    line = "{:<10} {:<25.2f} {:<25}\n".format(board_label, elapsed, num_winning)
                f.write(line)

            f.write("\nEnd of results.\n")
        print(f"\nAll results have been written to '{OUTPUT_TEXT_FILENAME}'.")
    except Exception as file_error:
        print(f"An error occurred while writing to {OUTPUT_TEXT_FILENAME}: {file_error}")

    # Write the CSV file for Excel (results_excel.csv)
    try:
        with open(OUTPUT_CSV_FILENAME, "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write header row
            writer.writerow(["Board", "Time (sec)", "Winning States", "Status"])

            for board, elapsed, num_winning, status in results:
                board_label = f"{board}x{board}"
                if status != "OK":
                    writer.writerow([board_label, status, "N/A", status])
                else:
                    writer.writerow([board_label, f"{elapsed:.2f}", num_winning, status])
        print(f"Results have also been written to '{OUTPUT_CSV_FILENAME}'.")
    except Exception as csv_error:
        print(f"An error occurred while writing to {OUTPUT_CSV_FILENAME}: {csv_error}")


if __name__ == '__main__':
    main()
