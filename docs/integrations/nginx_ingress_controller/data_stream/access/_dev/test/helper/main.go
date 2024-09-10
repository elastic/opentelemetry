package main

import (
	"bufio"
	"fmt"
	"os"
	"time"
)

func main() {
	scanner := bufio.NewScanner(os.Stdin)

	// Get the current timestamp
	timestamp := time.Now().UTC().Format("2006-01-02T15:04:05.000000000Z")

	for scanner.Scan() {
		// Prepend the current timestamp and "stdout F" to each line
		fmt.Printf("%s stdout F %s\n", timestamp, scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		fmt.Fprintln(os.Stderr, "Error reading from stdin:", err)
	}
}
