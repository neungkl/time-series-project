package main

import (
	"fmt"
	"io/ioutil"
	"math"
	"os"
	"strconv"
	"strings"
)

var Infinity = 9999999.0
var w1 float64
var w2 float64
var w3 float64

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func ReadFile(fileDir string) ([]int, [][]float64) {
	dataBytes, err := ioutil.ReadFile(fileDir)
	check(err)

	datas := strings.Split(string(dataBytes), "\n")

	var xLabel []int
	var xFeatures [][]float64

	for _, data := range datas {
		dataSplit := strings.Split(data, " ")

		var feature []float64

		j := 0
		for _, d := range dataSplit {
			if len(d) == 0 {
				continue
			}
			d = strings.Replace(d, "\r", "", -1)
			numF, err := strconv.ParseFloat(d, 64)
			check(err)
			if j == 0 {
				num := int(numF)
				xLabel = append(xLabel, num)
			} else {
				feature = append(feature, numF)
			}
			j = j + 1
		}

		xFeatures = append(xFeatures, feature)
	}

	return xLabel, xFeatures
}

func Dtw(x []float64, y []float64) float64 {
	xLen := len(x)
	yLen := len(y)

	dist := [][]float64{}
	dp := [][]float64{}

	for iy := 0; iy < yLen; iy++ {
		ddist := []float64{}
		ddp := []float64{}
		for ix := 0; ix < xLen; ix++ {
			ddist = append(ddist, math.Sqrt((x[ix]-y[iy])*(x[ix]-y[iy])))
			ddp = append(ddp, Infinity)
		}
		dist = append(dist, ddist)
		dp = append(dp, ddp)
	}

	dp[0][0] = dist[0][0]

	for iy := 0; iy < yLen; iy++ {
		for ix := 0; ix < xLen; ix++ {
			if ix > 0 {
				dp[iy][ix] = math.Min(dp[iy][ix], dp[iy][ix-1]+w1*dist[iy][ix])
			}
			if iy > 0 {
				dp[iy][ix] = math.Min(dp[iy][ix], dp[iy-1][ix]+w3*dist[iy][ix])
			}
			if ix > 0 && iy > 0 {
				dp[iy][ix] = math.Min(dp[iy][ix], dp[iy-1][ix-1]+w2*dist[iy][ix])
			}
		}
	}

	return dp[yLen-1][xLen-1]
}

var xLabel []int
var yLabel []int
var xFeatures [][]float64
var yFeatures [][]float64

func DtwFindClass(y []float64) int {
	bestClass := -1
	bestDist := Infinity

	for i := 0; i < len(xFeatures); i++ {
		dist := Dtw(xFeatures[i], y)
		// fmt.Println(xs[i])
		// fmt.Println(dist)

		if dist < bestDist {
			bestDist = dist
			bestClass = xLabel[i]
		}
	}

	return bestClass
}

func DtwAll() {
	correct := 0
	total := len(yLabel)
	// total := 5

	dist := make(chan int, 6)
	res := make(chan int)
	finish := make(chan int)

	go func() {
		for i := 0; i < total; i++ {
			correct += <-res
		}

		fmt.Printf("Result %v: %v/%v\n", float64(correct)/float64(total), correct, total)
		finish <- 0
	}()

	for i := 0; i < total; i++ {
		dist <- i
		go func(is int) {
			class := DtwFindClass(yFeatures[is])

			if (is+1)%10 == 0 {
				fmt.Printf("%d: %d %d\n", is+1, class, yLabel[is])
			}

			if class == yLabel[is] {
				res <- 1
			} else {
				res <- 0
			}
			<-dist
		}(i)
	}

	<-finish
	close(res)
	close(dist)
	close(finish)
}

func main() {
	xLabel, xFeatures = ReadFile("../data/CBF_TRAIN")
	yLabel, yFeatures = ReadFile("../data/CBF_TEST")

	if len(os.Args) < 4 {
		panic("Arguments not enough")
	}

	var err error
	w1, err = strconv.ParseFloat(os.Args[1], 64)
	check(err)
	w2, err = strconv.ParseFloat(os.Args[2], 64)
	check(err)
	w3, err = strconv.ParseFloat(os.Args[3], 64)
	check(err)

	fmt.Printf("w1: %v, w2: %v, w3: %v\n", w1, w2, w3)

	DtwAll()
}
