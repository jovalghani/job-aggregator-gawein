/// Job Model
/// Represents a job listing from the API
class Job {
  final int id;
  final String title;
  final String company;
  final String location;
  final String description;
  final int? salaryMin;
  final int? salaryMax;
  final String applyUrl;
  final List<String> skills;
  final String experienceLevel;
  final bool isRemote;
  final DateTime createdAt;

  Job({
    required this.id,
    required this.title,
    required this.company,
    required this.location,
    required this.description,
    this.salaryMin,
    this.salaryMax,
    required this.applyUrl,
    this.skills = const [],
    this.experienceLevel = 'unknown',
    this.isRemote = false,
    required this.createdAt,
  });

  factory Job.fromJson(Map<String, dynamic> json) {
    return Job(
      id: json['id'] as int,
      title: json['title'] as String,
      company: json['company'] as String,
      location: json['location'] as String? ?? 'Unknown',
      description: json['description'] as String? ?? '',
      salaryMin: json['salary_min'] as int?,
      salaryMax: json['salary_max'] as int?,
      applyUrl: json['apply_url'] as String,
      skills: json['skills'] != null 
          ? List<String>.from(json['skills']) 
          : [],
      experienceLevel: json['experience_level'] as String? ?? 'unknown',
      isRemote: json['is_remote'] as bool? ?? false,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }

  /// Format salary range for display
  String get salaryRange {
    if (salaryMin == null && salaryMax == null) {
      return 'Salary not disclosed';
    }
    
    final formatter = _formatCurrency;
    
    if (salaryMin != null && salaryMax != null) {
      return '${formatter(salaryMin!)} - ${formatter(salaryMax!)}';
    } else if (salaryMin != null) {
      return 'From ${formatter(salaryMin!)}';
    } else {
      return 'Up to ${formatter(salaryMax!)}';
    }
  }

  String _formatCurrency(int amount) {
    if (amount >= 1000000) {
      return 'Rp ${(amount / 1000000).toStringAsFixed(0)} jt';
    } else if (amount >= 1000) {
      return 'Rp ${(amount / 1000).toStringAsFixed(0)} rb';
    }
    return 'Rp $amount';
  }

  /// Get experience level display text
  String get experienceLevelDisplay {
    switch (experienceLevel.toLowerCase()) {
      case 'junior':
        return 'Junior (0-2 years)';
      case 'mid':
        return 'Mid-Level (2-5 years)';
      case 'senior':
        return 'Senior (5+ years)';
      default:
        return 'All Levels';
    }
  }
}
