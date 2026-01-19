import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import '../models/job.dart';

/// Job Service
/// Handles API communication with the FastAPI backend
class JobService extends ChangeNotifier {
  // API Configuration
  // Change this to your backend URL
  // static const String baseUrl = 'http://10.0.2.2:8000'; // Android emulator localhost
  static const String baseUrl =
      'http://localhost:8000'; // Web browser / iOS simulator
  // static const String baseUrl = 'https://your-api.com'; // Production

  List<Job> _jobs = [];
  bool _isLoading = false;
  String? _error;
  int _currentPage = 1;
  int _totalJobs = 0;
  final int _perPage = 10;

  // Getters
  List<Job> get jobs => _jobs;
  bool get isLoading => _isLoading;
  String? get error => _error;
  int get currentPage => _currentPage;
  int get totalJobs => _totalJobs;
  bool get hasMore => _jobs.length < _totalJobs;

  /// Fetch jobs from API
  Future<void> fetchJobs({
    String? keyword,
    String? location,
    int? minSalary,
    bool refresh = false,
  }) async {
    if (refresh) {
      _currentPage = 1;
      _jobs = [];
    }

    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final queryParams = {
        'page': _currentPage.toString(),
        'per_page': _perPage.toString(),
        if (keyword != null && keyword.isNotEmpty) 'keyword': keyword,
        if (location != null && location.isNotEmpty) 'location': location,
        if (minSalary != null) 'min_salary': minSalary.toString(),
      };

      final uri =
          Uri.parse('$baseUrl/jobs').replace(queryParameters: queryParams);

      final response = await http.get(
        uri,
        headers: {'Content-Type': 'application/json'},
      ).timeout(const Duration(seconds: 30));

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final jobsJson = data['jobs'] as List;
        final newJobs = jobsJson.map((j) => Job.fromJson(j)).toList();

        if (refresh) {
          _jobs = newJobs;
        } else {
          _jobs.addAll(newJobs);
        }

        _totalJobs = data['total'] as int;
        _currentPage++;
        _error = null;
      } else {
        _error = 'Failed to load jobs: ${response.statusCode}';
      }
    } catch (e) {
      _error = 'Connection error: ${e.toString()}';
      if (kDebugMode) {
        print('Error fetching jobs: $e');
      }
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  /// Fetch single job by ID
  Future<Job?> fetchJobById(int id) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/jobs/$id'),
        headers: {'Content-Type': 'application/json'},
      ).timeout(const Duration(seconds: 30));

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return Job.fromJson(data);
      }
    } catch (e) {
      if (kDebugMode) {
        print('Error fetching job $id: $e');
      }
    }
    return null;
  }

  /// Load more jobs (pagination)
  Future<void> loadMore() async {
    if (!_isLoading && hasMore) {
      await fetchJobs();
    }
  }

  /// Refresh jobs list
  Future<void> refresh() async {
    await fetchJobs(refresh: true);
  }

  /// Clear error
  void clearError() {
    _error = null;
    notifyListeners();
  }
}
