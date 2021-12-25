package main

import (
	"time"

	blinkt "github.com/alexellis/blinkt_go"
	"github.com/gleich/lumber/v2"
)

func main() {
	log := lumber.NewCustomLogger()
	log.Timezone = time.Local

	// Setup display
	display := blinkt.NewBlinkt(0.1)
	display.SetClearOnExit(true)
	display.Setup()
	display.Clear()
	log.Success("Setup dislay")

	oddRed := false
	for {
		for i := 0; i < 8; i++ {
			if i%2 == 0 {
				if oddRed {
					display.SetPixel(i, 0, 255, 0)
				} else {
					display.SetPixel(i, 255, 0, 0)
				}
			} else {
				if oddRed {
					display.SetPixel(i, 255, 0, 0)
				} else {
					display.SetPixel(i, 0, 255, 0)
				}
			}
		}
		display.Show()
		log.Success("Updated lights")
		time.Sleep(1 * time.Second)
		oddRed = !oddRed
	}
}
