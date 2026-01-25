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

### Templates
```
0111 1111 0000 0Spp
```
No shelter 

```
0111 1111 001S ppss
```
Has shelter

### Empty Ground
```
0111 1111 1111 111b
```

b: 0 for concrete, 1 for natural

## 0x8000 - 0xFFFE: Wuhu Station (2015)
````
1xxx xxxx xpps svvv
````

Where:
* `x` is the tile id (0-239)
* `v` is the minor feature variant (0-7)
    * 0 for platform connectors [no track]
    * 1 and 2 for one-sided platforms [has track]
    * 3 for two-sided platforms [has track]
    * 4 for regular ground-level buildings [no track]
      Potentially slated for reassignment, since this is very similar to the "with solid ground floor" class below
    * 5 for narrow ground-level buildings + platform [has track]
    * 6 for narrow ground-level buildings [has track]
    * 7 for narrow ground-level buildings on both sides [has track]

````
1111 1101 xxxx xxxx
````
With no ground-level buildings at all (waypoints).

````
1111 1100 xxxx xxxx
````
With no ground-level buildings nor railroad.

````
1111 1011 xxxx xxxx
````
With solid ground floor.

### 0xFE00 - 0xFEFE: Flexible Partial-Templates
#### Half Templates
````
1111 1111 0abc ppss
````

Where:
* `a` is far or near side
* `b` is whether the front (or back) row is traversable
* `c` is presence or absence of side platforms

#### Central Templates
````
1111 1111 100a ppss
````

Where:
* `a` is presence or absence of side platforms

### 0xFF00 - 0xFFFE: Flexible Templates
#### Semitraversable Templates
````
1111 1110 0000 ppss
````
With side platforms

````
1111 1110 0001 ppss
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
