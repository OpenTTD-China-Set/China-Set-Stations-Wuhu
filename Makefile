.PHONY: rebuild all station clean_station clean doc.station

rebuild: clean all

all: station.grf

station: clean_station station.grf

clean_station:
	rm -f station.grf

clean:
	rm -f *.grf

doc.station:
	python3 -m station.dovemere_gen doc
	cd docs; make html

station.grf:
	python3 -m station.dovemere_gen gen
