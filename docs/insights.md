## Early Failure Detection Is a Systems Problem

### Overview
Early failure detection in complex systems is often treated as a modeling problem. This analysis shows that the dominant challenge is decision robustness rather than signal availability.

Using the NASA C-MAPSS turbofan dataset, degradation detection is evaluated through sustained evidence, variability across engines, and explicit false-positive control.

### Sensor Behavior Is Heterogeneous
Sensors behave differently as failure approaches. Some show smooth monotonic drift. Others remain stable until late-stage failure. Some provide early deviation for certain engines but not others.

Ranking sensors by median warning time shows that the earliest detectors provide roughly 95 cycles of warning on average. However, these sensors often exhibit wide variability across engines, making them unreliable as sole alarms.

Other sensors alarm slightly later but do so consistently across nearly all engines.

The key insight is that early detection and reliability are often in tension at the single-sensor level.

### Sustained Alarms Matter
Naive thresholding causes nearly all sensors to alarm eventually due to noise.

Requiring sustained deviation over multiple cycles dramatically improves alarm quality. Alarms become more interpretable, less sensitive to noise, and more consistent across engines.

This change converts raw sensor data into decision-grade signals.

### Composite Health Scoring Improves Reliability
To balance early detection and consistency, a composite health score is constructed as the mean absolute deviation across drifting sensors.

After rolling smoothing and sustained alarm logic, the composite score alarms on all engines with a median warning time of approximately 81 cycles. The healthy false-positive rate is zero percent.

While slightly later than the earliest single-sensor alarms, the composite alarm is significantly more reliable and easier to govern.

### False Positives Are a Design Constraint
Rather than tuning thresholds visually, false positives are explicitly measured during healthy operation. Alarm thresholds are selected to satisfy a target false-positive rate.

This reframes detection as a constrained design problem rather than an optimization problem.

### Practical Monitoring Strategy
A practical monitoring strategy based on these results would use the composite health score as the primary alarm. Individual sensor alarms would support diagnosis and root cause analysis. Thresholds would be governed by false-positive tolerances rather than visual intuition. Warning-time distributions would be communicated instead of single alarm points.

### Conclusion
Early failure detection is not about identifying the most sensitive sensor. It is about designing systems that balance sensitivity, robustness, and trust.

This project demonstrates that sustained logic, per-engine normalization, and composite scoring can transform noisy sensor data into reliable monitoring signals suitable for real-world deployment.
