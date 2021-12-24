package main

import (
	"fmt"
	"time"

	"github.com/gleich/blinkt_christmas/pkg/conf"
	"github.com/gleich/lumber/v2"
)

func main() {
	log := lumber.NewCustomLogger()
	log.Timezone = time.Local
	config, err := conf.Read(log)
	if err != nil {
		log.Fatal(err, "Failed to load config file")
	}
	fmt.Println("on:", *config.On)
}
