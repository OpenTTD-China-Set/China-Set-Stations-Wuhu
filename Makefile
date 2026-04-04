.PHONY: rebuild all station clean_station clean doc.station profile report.station cc.station

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
	ulimit -n 4096; python3 -m station.dovemere_gen gen

profile.station:
	python3 -m cProfile -o .prof/station.prof -m station.dovemere_gen gen

report.station:
	python3 -c "import pstats; pstats.Stats('.prof/station.prof').sort_stats('cumulative').print_stats(50)"

report_dot.station:
	gprof2dot -f pstats .prof/station.prof | dot -Tpng -o .prof/station_gen_prof.png

pprofile.station:
	pprofile --statistic .01 -m station.dovemere_gen gen | tee .prof/station_pprofile.txt

cc.station:
	opencc -i station/lang/chinese.lng -o station/lang/traditional_chinese.lng -c station/lang/opencc_config/s2t.json
	sed -i 's/##grflangid.*/##grflangid 0x0C/' station/lang/traditional_chinese.lng
