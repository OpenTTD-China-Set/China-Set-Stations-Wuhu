# Stations
## 0x00 - 0xFF: pre-14.0 compatibilty mode

## 0x7000 - 0x7FFF: platforms
```
0111 0pp0 ssrd 000i
```
Where:
* `pp` is the Platform Type (0-3)
* `ss` is the Shelter Type (0-3)
* `r` is whether the platform has a rail-facing surface
* `d` is whether the tile contains two platforms
* `i` is the platform location (north or south), only relevant for d=0

```
0111 100p prr0 ssSi
```
Where:
* `pp` is the Platform Type (0-3)
* `rr` is whether each of the two platforms has a rail-facing surface
* `ss` is the Shelter Type (0-3)
* `S` is whether both platforms have shelters
* `i` is the platform location (north or south), only relevant for asymmetrical cases

```
0111 1010 0000 ppdi
```
entry.id = 0x7A00 + pid * 0x4 + ssid * 0x2 + i

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
