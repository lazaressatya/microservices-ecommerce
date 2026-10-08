package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

var collection *mongo.Collection

func main() {

	mongoURI := os.Getenv(
		"MONGODB_URI",
	)

	if mongoURI == "" {
		mongoURI =
			"mongodb://inventory-mongodb:27017"
	}

	client, err :=
		mongo.Connect(
			context.Background(),
			options.Client().ApplyURI(mongoURI),
		)

	if err != nil {
		log.Fatal(err)
	}

	collection =
		client.Database("inventorydb").
			Collection("inventory")

	http.HandleFunc("/", home)
	http.HandleFunc("/health", health)
	http.HandleFunc("/inventory", inventory)

	fmt.Println(
		"Inventory Service running on port 3005",
	)

	log.Fatal(
		http.ListenAndServe(
			":3005",
			nil,
		),
	)
}

func home(
	w http.ResponseWriter,
	r *http.Request,
) {

	w.Header().Set(
		"Content-Type",
		"application/json",
	)

	fmt.Fprint(
		w,
		`{"service":"Inventory Service","status":"running"}`,
	)
}

func health(
	w http.ResponseWriter,
	r *http.Request,
) {

	w.Header().Set(
		"Content-Type",
		"application/json",
	)

	fmt.Fprint(
		w,
		`{"service":"inventory-service","status":"UP"}`,
	)
}

func inventory(
	w http.ResponseWriter,
	r *http.Request,
) {

	cursor, err :=
		collection.Find(
			context.Background(),
			bson.M{},
		)

	if err != nil {
		http.Error(
			w,
			err.Error(),
			http.StatusInternalServerError,
		)

		return
	}

	defer cursor.Close(context.Background())

	w.Header().Set(
		"Content-Type",
		"application/json",
	)

	fmt.Fprint(w, "[")

	first := true

	for cursor.Next(context.Background()) {

		if !first {
			fmt.Fprint(w, ",")
		}

		first = false

		var item bson.M

		if err := cursor.Decode(&item); err != nil {
			continue
		}

		fmt.Fprintf(
			w,
			`{"productId":"%v","quantity":"%v"}`,
			item["productId"],
			item["quantity"],
		)
	}

	fmt.Fprint(w, "]")
}