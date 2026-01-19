// Widget tests for Job Aggregator App
//
// These tests verify that the main UI components render correctly.

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:job_aggregator/main.dart';

void main() {
  testWidgets('App renders correctly with Job Aggregator title',
      (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const JobAggregatorApp());

    // Wait for the widget tree to settle
    await tester.pumpAndSettle();

    // Verify that the app title is displayed
    expect(find.text('Job Aggregator'), findsOneWidget);

    // Verify that the subtitle is displayed
    expect(find.text('Temukan pekerjaan impianmu'), findsOneWidget);
  });

  testWidgets('Search bar is present', (WidgetTester tester) async {
    // Build our app
    await tester.pumpWidget(const JobAggregatorApp());

    // Wait for the widget tree to settle
    await tester.pumpAndSettle();

    // Verify search bar hint text is present
    expect(find.text('Cari pekerjaan...'), findsOneWidget);
  });

  testWidgets('FloatingActionButton is present', (WidgetTester tester) async {
    // Build our app
    await tester.pumpWidget(const JobAggregatorApp());

    // Wait for the widget tree to settle
    await tester.pumpAndSettle();

    // Verify FAB is present
    expect(find.byType(FloatingActionButton), findsOneWidget);
  });

  testWidgets('App shows error or jobs after loading',
      (WidgetTester tester) async {
    // Build our app
    await tester.pumpWidget(const JobAggregatorApp());

    // Wait for initial frame
    await tester.pump();

    // Pump and settle to wait for async operations
    await tester.pumpAndSettle(const Duration(seconds: 2));

    // After loading, either we see jobs or an error message
    // Since we're testing without backend, we expect error state
    final hasError =
        find.textContaining('Connection error').evaluate().isNotEmpty ||
            find.textContaining('Gagal memuat').evaluate().isNotEmpty;
    final hasJobs = find.textContaining('lowongan').evaluate().isNotEmpty;

    // Either error or jobs should be displayed
    expect(hasError || hasJobs, isTrue);
  });
}
