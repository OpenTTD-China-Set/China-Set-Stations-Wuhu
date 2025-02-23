rebuild: clean all

all: station.grf

station: clean_station station.grf

clean_station:
	rm -f station.grf

clean:
	rm -f *.grf

doc.station:
	python3 -m station.dovemere_gen doc

station.grf:
	python3 -m station.dovemere_gen gen

profile.station:
	python3 -m cProfile -o .prof/station_gen.prof -m station.dovemere_gen gen
	gprof2dot -f pstats .prof/station_gen.prof | dot -Tpng -o .prof/station_gen_prof.png

pprofile.station:
	pprofile --statistic .01 -m station.dovemere_gen gen | tee .prof/station_pprofile.txt
