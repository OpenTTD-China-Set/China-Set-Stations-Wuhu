# Common Denotations
* `pp` is the Platform Type (0-3)
* `ss` is the Shelter Type (0-3)
# Stations
## 0x00 - 0xFF: pre-14.0 compatibilty mode

## 0x7000 - 0x7FFF: platforms
### Rail with one platform
```
0111 0pp0 ssrd 000i
```
Where:
* `r` is whether the platform has a rail-facing surface
* `d` is whether the tile contains two platforms
* `i` is the platform location (north or south), only relevant for d=0

### Rail with two platforms
```
0111 100p prr0 ssSi
```
Where:
* `ss` is the Shelter Type (0-3)
* `S` is whether both platforms have shelters
* `i` is the platform location (north or south), only relevant for asymmetrical cases

### No rail, no shelter
```
0111 1010 0000 ppdi
```

Where:
* `d` is whether the tile contains two platforms
* `i` is the platform location (north or south), only relevant for asymmetrical cases

### No rail, has shelter
````
0111 1011 0ppd ssli
````
entry.id = 0x7B00 + pid * 0x20 + ssid * 0x10 + sid * 0x4 + lid * 0x2 + i

## 0x8000 - 0xFFFE: Wuhu Station (2015)

### 0xFF00 - 0xFFFE: Flexible Templates
#### Semitraversable Templates
````
1111 1111 0000 ppss
````
With side platforms

````
1111 1111 0001 ppss
````
Without side platforms

#### Traversable Templates
````
1111 1111 0010 ppss
````
With side platforms

````
1111 1111 0011 ppss
````
Without side platforms

#### Non-traversable one-row stations
````
1111 1111 0100 ppss
````
Front side

````
1111 1111 0101 ppss
````
Back side

````
1111 1111 0110 ppss
````
Front side, no platform

````
1111 1111 0111 ppss
````
Back side, no platform

#### Traversable one-row stations
````
1111 1111 1000 ppss
````
Front side

````
1111 1111 1001 ppss
````
Back side

````
1111 1111 1010 ppss
````
Front side, no platform

````
1111 1111 1011 ppss
````
Back side, no platform
