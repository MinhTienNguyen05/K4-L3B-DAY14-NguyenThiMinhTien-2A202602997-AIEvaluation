# Day 14 — Exercises

## AI Evaluation & Benchmarking · Lab Worksheet

**Thời gian làm bài:** 9:15–12:00

**Domain:** OrbitTech Store Customer Support

Điền trực tiếp câu trả lời vào file này. Golden dataset 20 QA được viết một lần
duy nhất trong `golden_dataset.json`, không chép lại toàn bộ vào Markdown.

---

Từ 9:15–9:30, cài môi trường và chạy baseline tests theo `guide_lab.md`.

---

## Part 1 — Warm-up (9:30–9:45)

### Exercise 1.1 — RAGAS Metric Thresholds

Theo bài giảng:

- 0.8–1.0: Good — monitor, maintain.
- 0.6–0.8: Needs work — analyze failures, iterate.
- Dưới 0.6: Significant issues — investigate.

Với từng metric, xác định khi nào score thấp có thể chấp nhận và khi nào là
critical.

| Metric            | Acceptable Low Score Scenario                                                                                                                          | Critical Low Score Scenario                                                                                                                                           | Action Required                                                                                                                                     |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| Faithfulness      | LLM diễn đạt lại bằng từ vựng hoặc cấu trúc câu khác biệt so với ngữ cảnh gốc nhưng bản chất thông tin không sai lệch.          | LLM tự bịa ra chính sách (hallucination) như tự ý kéo dài thời gian bảo hành, mâu thuẫn hoàn toàn với tài liệu.                                    | Tinh chỉnh System Prompt để ép buộc mô hình tuân thủ nghiêm ngặt ngữ cảnh (strict grounding), thêm quality gate chặn câu trả lời. |
| Answer Relevance  | Khách hàng hỏi câu quá chung chung, khiến LLM trả lời hơi dài dòng hoặc cung cấp thông tin mở rộng không thật sự sát ý.           | Trợ lý lạc đề hoàn toàn, cung cấp thông tin cho một sản phẩm/chính sách khác hoặc lảng tránh câu hỏi.                                             | Cập nhật hướng dẫn cho LLM (prompt) để tập trung trả lời trực tiếp, hoặc thêm bước đánh giá lại query intent                    |
| Context Recall    | Retriever bỏ sót một vài đoạn thông tin phụ trợ, nhưng vẫn lấy được đoạn chứa luận điểm chính để LLM trả lời.                | Mất hoàn toàn đoạn tài liệu cốt lõi chứa đáp án (ví dụ không tìm thấy chính sách đổi trả), khiến LLM trả lời sai hoặc báo "không biết". | Tối ưu hóa chiến lược Chunking, cải thiện embedding model, hoặc kết hợp thêm từ khóa metadata.                                        |
| Context Precision | Tài liệu đúng bị xếp ở vị trí thấp (Top 4-5) thay vì Top 1, nhưng độ dài context window vẫn chứa đủ nội dung để LLM phân tích. | Toàn bộ Top-K kết quả truy xuất là nhiễu, đẩy thông tin quan trọng ra khỏi context window của LLM.                                                       | Áp dụng cơ chế Reranking (như Cross-Encoder) để sắp xếp lại độ ưu tiên của kết quả, hoặc dùng Hybrid Search.                     |
| Completeness      | Bỏ sót một chi tiết nhỏ hoặc không quan trọng khi đối mặt với câu hỏi gồm quá nhiều vế phức tạp.                                   | Bỏ qua một bước bắt buộc trong quy trình (ví dụ: quên nhắc khách hàng mang theo hóa đơn khi đi bảo hành).                                          | Yêu cầu LLM chia nhỏ câu hỏi thành các ý (Chain of Thought) để đảm bảo rà soát và trả lời đầy đủ mọi vế.                    |

### Exercise 1.2 — Bias trong LLM-as-a-Judge

Ba bias thường gặp:

- Position bias: judge ưu tiên answer xuất hiện trước.
- Verbosity bias: judge ưu tiên answer dài hơn.
- Self-preference: judge ưu tiên output giống chính model đó.

**Câu 1: Thiết kế experiment phát hiện position bias với ít nhất hai conditions.**

> * **Condition 1 (Original Order):** Cung cấp cho LLM Judge hai câu trả lời theo thứ tự hiển thị là [Câu trả lời A] trước, [Câu trả lời B] sau, và yêu cầu chọn câu tốt hơn.
> * **Condition 2 (Swapped Order):** Giữ nguyên câu hỏi và nội dung hai câu trả lời, nhưng đảo ngược thứ tự đưa vào prompt: [Câu trả lời B] trước, [Câu trả lời A] sau.
> * **Đánh giá:** Tính toán tỉ lệ chiến thắng (win rate). Nếu tỉ lệ một câu trả lời (ví dụ A) được chọn giảm đi đáng kể khi nó bị đẩy xuống vị trí thứ 2, điều đó chứng tỏ LLM Judge đang bị thiên vị vị trí ưu tiên lựa chọn đáp án xuất hiện đầu tiên (hoặc cuối cùng).

**Câu 2: Làm thế nào giảm verbosity bias bằng rubric design?**

> Bổ sung các tiêu chí phạt sự lan man và thưởng cho sự súc tích trực tiếp vào hệ thống chấm điểm.
>
> * **Thêm tiêu chí cụ thể:** Đưa các tiêu chí như "Tính súc tích" (Conciseness) hoặc "Mật độ thông tin" (Information Density) vào bộ tiêu chuẩn đánh giá.
> * **Explicit Instructions (Chỉ thị rõ ràng):** Cập nhật system prompt của LLM Judge với các yêu cầu như: *"Trừ điểm nếu câu trả lời chứa thông tin dư thừa, lặp lại hoặc không liên quan. Không tự động cho điểm cao hơn đối với các câu trả lời dài mà không bổ sung thêm giá trị cốt lõi giải quyết đúng trọng tâm câu hỏi."*

**Câu 3: Tại sao cần calibrate LLM judge với human labels?**

 Để đảm bảo thước đo tự động của máy đồng cấp với nhận thức và Ground Truth.

* LLM Judge có thể tự tin chấm điểm sai hoặc bị ảnh hưởng bởi các bias do dữ liệu huấn luyện của chính nó. Việc so sánh điểm của LLM với Human Labels giúp đo lường hệ số tương quan (ví dụ: Pearson hoặc Spearman correlation). Nếu độ tương quan thấp, bạn sẽ biết bộ Rubric hoặc Prompt đánh giá hiện tại đang có vấn đề (chấm quá lỏng, quá chặt, hoặc sai tiêu chí) và cần phải được tinh chỉnh lại trước khi đưa vào chạy pipeline tự động hóa ở quy mô lớn.

### Exercise 1.3 — Evaluation trong CI/CD

**Câu 1: Chọn threshold để block deployment.**

| Metric           | Threshold | Lý do                                                                                                                                                                                                                                                                                                                            |
| ---------------- | --------: | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Faithfulness     |       0.9 | Đây là chỉ số quan trọng nhất. Nếu hệ thống tự bịa ra thông tin về giá cả, bảo hành hay chính sách, cửa hàng sẽ chịu rủi ro về uy tín và tài chính. Cần một ngưỡng cực kỳ khắt khe để đảm bảo câu trả lời luôn trung thành với Knowledge Base.                                   |
| Answer Relevance |      0.85 | Việc trợ lý trả lời vòng vo hoặc lạc đề gây trải nghiệm xấu, nhưng ít nghiêm trọng hơn việc nói sai sự thật. Ngưỡng 0.85 đủ cao để đảm bảo hệ thống hiểu và giải quyết đúng trọng tâm nhu cầu của khách hàng, đồng thời cho phép một chút linh hoạt trong cách diễn đạt. |
| Completeness     |       0.8 | Khách hàng thường chấp nhận việc AI trả lời thiếu một vài chi tiết nhỏ (và họ có thể hỏi thêm để làm rõ). Ngưỡng 0.80 đảm bảo các vế chính của câu hỏi phức tạp được giải quyết, không cần quá khắt khe chặn deploy nếu thiếu một ý phụ.                                      |

**Câu 2: Khi nào dùng offline evaluation, online evaluation và human review?**

> * **Offline Evaluation (Đánh giá ngoại tuyến):** Dùng trong giai đoạn phát triển và quy trình CI/CD trước khi đưa hệ thống lên production. Đánh giá được thực hiện trên Golden Dataset để kiểm tra các thay đổi mới (như đổi prompt, đổi mô hình, thay thuật toán chunking) có làm giảm chất lượng hệ thống so với phiên bản trước hay không.
> * **Online Evaluation (Đánh giá trực tuyến):** Dùng khi hệ thống đang chạy thực tế. Mục tiêu là giám sát hiệu suất liên tục dựa trên các tương tác thật của người dùng. Phương pháp này thường sử dụng các tín hiệu ngầm (như thời gian đọc, click) hoặc phản hồi trực tiếp (thumbs up/down) kết hợp với LLM Judge chạy ngầm để phát hiện xu hướng câu hỏi mới hoặc các lỗi mà tập dữ liệu offline chưa bao phủ được.
> * **Human Review (Đánh giá bởi con người):** Dùng để hiệu chuẩn độ chính xác của công cụ LLM-as-a-Judge, kiểm toán định kỳ chất lượng hệ thống, hoặc xử lý các trường hợp hệ thống gặp lỗi nghiêm trọng (edge cases/low confidence). Con người cũng cần tham gia khi đánh giá các truy vấn mang tính nhạy cảm, phức tạp cao mà các chỉ số tự động không thể nắm bắt trọn vẹn ngữ cảnh.

---

## Part 2 — Core Coding (9:45–10:40)

Hoàn thiện các TODO bắt buộc trong `template.py`.

### Task 1 — Data Models

- `QAPair`: question, expected answer, gold context, metadata và retrieved contexts.
- `EvalResult`: answer-side scores, optional retrieval scores, pass/failure fields.
- `overall_score()`: trung bình Faithfulness, Relevance và Completeness.

### Task 2 — RAGASEvaluator

Answer-side:

- `evaluate_faithfulness(answer, context)`
- `evaluate_relevance(answer, question)`
- `evaluate_completeness(answer, expected)`

Retrieval-side:

- `evaluate_context_recall(contexts, expected)`
- `evaluate_context_precision(contexts, expected)`

Full pipeline:

- `run_full_eval(..., contexts=None)` luôn tính ba answer metrics.
- Nếu có `contexts`, tính và lưu thêm Context Recall và Context Precision.
- Retrieval scores không làm thay đổi `overall_score()` và pass rule gốc.

### Task 3 — LLMJudge

- `score_response(question, answer, rubric)`
- `detect_bias(scores_batch)`

### Task 4 — BenchmarkRunner

- `run(qa_pairs, agent_fn, evaluator)`
- `generate_report(results)`
- `run_regression(new_results, baseline_results)`
- `identify_failures(results, threshold)`

`BenchmarkRunner.run()` phải truyền `pair.retrieved_contexts` vào
`run_full_eval()`. Report phải có average của hai retrieval metrics.

### Task 5 — FailureAnalyzer

- `categorize_failures(failures)`
- `find_root_cause(failure)`
- `generate_improvement_suggestions(failures)`
- `generate_improvement_log(failures, suggestions)`

Kiểm tra:

```bash
pytest tests/ -v
```

`rerank_by_overlap()` là TODO bonus của Exercise 3.5. Test tương ứng được skip
nếu bạn chưa làm bonus.

---

## Part 3 — Golden Dataset & Real Benchmark (10:40–11:35)

### Exercise 3.1 — Build the Golden Dataset

Thiết kế và validate dataset theo Mục 5–6 trong `guide_lab.md`. Nội dung 20 QA
được điền trực tiếp trong `golden_dataset.json`; phần dưới chỉ ghi lại kết quả
và quyết định thiết kế, không chép lại toàn bộ QA.

**Kết quả dataset**

| Hạng mục                         | Kết quả   |
| ---------------------------------- | ----------- |
| Tổng số records                  | ____ / 20   |
| Easy                               | ____ / 5    |
| Medium                             | ____ / 7    |
| Hard                               | ____ / 5    |
| Adversarial                        | ____ / 3    |
| Source documents được sử dụng | ____ / 10   |
| Validator status                   | PASS / FAIL |

**Ba case đại diện cho quyết định thiết kế**

| ID | Difficulty | Source document(s) | Vì sao case phù hợp với difficulty/attack type? |
| -- | ---------- | ------------------ | --------------------------------------------------- |
|    |            |                    |                                                     |
|    |            |                    |                                                     |
|    |            |                    |                                                     |

**Điểm khó nhất khi xây dựng expected answer hoặc evidence là gì?**

> *Câu trả lời:*

**Xác nhận:**

- [ ] Mọi claim trong expected answer đều có evidence hỗ trợ.
- [ ] Không có questions trùng ý và không dùng kiến thức ngoài corpus.
- [ ] `python validate_golden_dataset.py` báo `PASS`.

### Exercise 3.2 — Benchmark Run

Chạy:

```bash
python domain_assistant.py
python evaluate_answers.py
```

Copy bảng terminal vào đây hoặc điền từ `artifacts/benchmark_results.json`.

| ID  | Question (short) | Ctx Recall | Ctx Precision | Faithfulness | Relevance | Completeness | Overall | Passed? | Failure Type |
| --- | ---------------- | ---------: | ------------: | -----------: | --------: | -----------: | ------: | ------- | ------------ |
| E01 |                  |            |               |              |           |              |         |         |              |
| E02 |                  |            |               |              |           |              |         |         |              |
| E03 |                  |            |               |              |           |              |         |         |              |
| E04 |                  |            |               |              |           |              |         |         |              |
| E05 |                  |            |               |              |           |              |         |         |              |
| M01 |                  |            |               |              |           |              |         |         |              |
| M02 |                  |            |               |              |           |              |         |         |              |
| M03 |                  |            |               |              |           |              |         |         |              |
| M04 |                  |            |               |              |           |              |         |         |              |
| M05 |                  |            |               |              |           |              |         |         |              |
| M06 |                  |            |               |              |           |              |         |         |              |
| M07 |                  |            |               |              |           |              |         |         |              |
| H01 |                  |            |               |              |           |              |         |         |              |
| H02 |                  |            |               |              |           |              |         |         |              |
| H03 |                  |            |               |              |           |              |         |         |              |
| H04 |                  |            |               |              |           |              |         |         |              |
| H05 |                  |            |               |              |           |              |         |         |              |
| A01 |                  |            |               |              |           |              |         |         |              |
| A02 |                  |            |               |              |           |              |         |         |              |
| A03 |                  |            |               |              |           |              |         |         |              |

**Aggregate Report**

- Overall pass rate: ____%
- Avg Context Recall: ____
- Avg Context Precision: ____
- Avg Faithfulness: ____
- Avg Relevance: ____
- Avg Completeness: ____
- Failure type distribution: ____

**Ba cases có Overall Score thấp nhất**

1. ID: ____ | Score: ____ | Failure type: ____
2. ID: ____ | Score: ____ | Failure type: ____
3. ID: ____ | Score: ____ | Failure type: ____

**Nhận xét ngắn:** Metric nào yếu nhất? Kết quả gợi ý vấn đề nằm ở retrieval
hay generation?

> *Câu trả lời:*

### Exercise 3.3 — LLM-as-a-Judge Rubric Design

Thiết kế rubric domain-specific cho OrbitTech Customer Support. Mỗi mức phải
đủ cụ thể để hai người chấm độc lập có thể hiểu giống nhau.

Chọn 3–5 dimensions:

- [ ] Correctness
- [ ] Completeness
- [ ] Relevance
- [ ] Evidence/citation
- [ ] Actionability
- [ ] Safety/privacy
- [ ] Tone/clarity
- [ ] Dimension khác: __________

| Score | Tiêu chí domain-specific | Ví dụ response |
| ----: | -------------------------- | ---------------- |
|     5 |                            |                  |
|     4 |                            |                  |
|     3 |                            |                  |
|     2 |                            |                  |
|     1 |                            |                  |

**Ba edge cases khó chấm**

| Edge Case | Tại sao khó chấm? | Rubric xử lý thế nào? |
| --------- | -------------------- | ------------------------- |
|           |                      |                           |
|           |                      |                           |
|           |                      |                           |

**Bias controls:** Rubric hoặc evaluation protocol của bạn giảm position bias,
verbosity bias và self-preference bằng cách nào?

> *Câu trả lời:*

### Exercise 3.4 — Framework Comparison (Bonus +5)

Chỉ làm sau khi hoàn thành 3.1–3.3. Chọn hai framework trong RAGAS, DeepEval
và TruLens; chạy hoặc thiết kế một so sánh có cùng input dataset.

| Tiêu chí                    | Framework 1: ____ | Framework 2: ____ |
| ----------------------------- | ----------------- | ----------------- |
| Setup complexity              |                   |                   |
| Metrics available             |                   |                   |
| CI/CD integration             |                   |                   |
| Kết quả trên cùng dataset |                   |                   |
| Insight rút ra               |                   |                   |

- Scores có nhất quán không?
- Framework nào strict hơn và vì sao?
- Hai framework có tìm ra cùng failure cases không?

> *Phân tích:*

### Exercise 3.5 — Retrieval Reranking (Bonus +5)

Mục tiêu: kiểm tra việc đổi thứ tự chunks có tăng Context Precision mà không
thay đổi Context Recall hay không.

1. Chọn ít nhất 5 cases từ `artifacts/actual_answers.json`.
2. Tính Context Recall và Context Precision trước rerank.
3. Implement `rerank_by_overlap()` hoặc một reranker khác.
4. Rerank cùng tập chunks, không thêm hoặc xóa chunk.
5. Tính lại hai metrics và giải thích kết quả.

| ID            | Recall before | Recall after | Precision before | Precision after | Delta Precision |
| ------------- | ------------: | -----------: | ---------------: | --------------: | --------------: |
|               |               |              |                  |                 |                 |
|               |               |              |                  |                 |                 |
|               |               |              |                  |                 |                 |
|               |               |              |                  |                 |                 |
|               |               |              |                  |                 |                 |
| **Avg** |               |              |                  |                 |                 |

**Tại sao Recall dự kiến không đổi?**

> *Câu trả lời:*

**Khi nào reranking không đủ và cần sửa retriever/query/chunking?**

> *Câu trả lời:*

---

## Part 4 — Reflection (11:35–11:50)

Hoàn thành `reflection.md` bằng kết quả thật từ Exercise 3.2.

---

## Completion Checklist

Hoàn thành kiểm tra cuối trong khoảng 11:50–12:00.

- [ ] Tất cả required tests pass.
- [ ] `golden_dataset.json` validate thành công.
- [ ] Exercise 3.1 hoàn thành trong file JSON và bảng kết quả phía trên.
- [ ] Exercise 3.2 có năm metrics, aggregate report và ba cases thấp nhất.
- [ ] Exercise 3.3 có rubric 1–5 và bias controls.
- [ ] `reflection.md` có ba failure analyses và regression strategy.
- [ ] Đã copy `template.py` thành `solution/solution.py`.
- [ ] Exercise 3.4 và 3.5 chỉ làm nếu chọn bonus.
