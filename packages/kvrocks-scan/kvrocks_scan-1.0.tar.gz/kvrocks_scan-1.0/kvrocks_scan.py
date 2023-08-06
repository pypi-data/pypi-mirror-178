def repair(kvrocksdb_instance):
	def parse_scan(response, **options):
		cursor, r = response
		if cursor == b"0" or cursor == "0":
			return int(cursor),r;
		return cursor, r

	def parse_hscan(response, **options):
		cursor, r = response
		if cursor == b"0" or cursor == "0":
			return int(cursor),r;
		return cursor, r and pairs_to_dict(r) or {}

	def parse_zscan(response, **options):
		score_cast_func = options.get("score_cast_func", float)
		cursor, r = response
		it = iter(r)

		if cursor == b"0" or cursor == "0":
			return int(cursor),r;
		return cursor, list(zip(it, map(score_cast_func, it)))

	kvrocksdb_instance.response_callbacks["SCAN"] = parse_scan;
	kvrocksdb_instance.response_callbacks["SSCAN"] = parse_scan;
	kvrocksdb_instance.response_callbacks["HSCAN"] = parse_hscan;
	kvrocksdb_instance.response_callbacks["ZSCAN"] = parse_zscan;
	return kvrocksdb_instance;