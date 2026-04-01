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
	python3 -m station.dovemere_gen gen

profile.station:
	python3 -m cProfile -o station.prof -m station.dovemere_gen gen

report.station:
	python3 -c "import pstats; pstats.Stats('station.prof').sort_stats('cumulative').print_stats(50)"

cc.station:
	python3 -m agrf.localization.traditional_chinese -i station/lang/chinese.lng -o station/lang/traditional_chinese.lng
	sed -i 's/##grflangid.*/##grflangid 0x0C/' station/lang/traditional_chinese.lng
