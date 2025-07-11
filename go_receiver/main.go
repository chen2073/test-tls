package main

import (
	"bufio"
	"crypto/tls"
	"fmt"
	"log"
	"net"
	"os"
	"strings"
)

func main() {
	// host := os.Getenv("HOST")
	port := os.Getenv("PORT")

	address := fmt.Sprintf(":%s", port)

	// listener, err := net.Listen("tcp", address)
	// if err != nil {
	// 	println("err starting tcp server")
	// 	os.Exit(1)
	// }

	cert, err := tls.LoadX509KeyPair("/certs/server.crt", "/certs/server.key")
	if err != nil {
		log.Fatal(err)
	}

	config := &tls.Config{Certificates: []tls.Certificate{cert}}

	listener, err := tls.Listen("tcp", address, config)
	if err != nil {
		log.Fatal(err)
	}

	defer listener.Close()

	fmt.Printf("tls Server listening on :%s\n", port)

	for {
		// Accept incoming connections
		conn, err := listener.Accept()
		if err != nil {
			fmt.Printf("Error accepting connection: %v\n", err)
			continue
		}

		// Handle each connection in a separate goroutine
		go handleConnection(conn)
	}
}

func handleConnection(conn net.Conn) {
	defer conn.Close()

	clientAddr := conn.RemoteAddr().String()
	fmt.Printf("New client connected: %s\n", clientAddr)

	// Create a scanner to read messages line by line
	scanner := bufio.NewScanner(conn)

	for scanner.Scan() {
		message := strings.TrimSpace(scanner.Text())

		if message == "" {
			continue
		}

		fmt.Printf("Received from %s: %s\n", clientAddr, message)
	}

	if err := scanner.Err(); err != nil {
		fmt.Printf("Error reading from %s: %v\n", clientAddr, err)
	}

	fmt.Printf("Connection closed: %s\n", clientAddr)
}
