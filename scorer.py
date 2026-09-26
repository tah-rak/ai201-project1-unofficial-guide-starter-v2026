"""Simple answer scorer for the Milestone 6 evaluation."""


def judge(question, expects, answer, results) -> bool:
    """Pass when the answer contains the expected phrase and a source name."""
    answer_text = answer.casefold()
    expected_text = expects.strip().casefold()
    source_names = [result.source.casefold() for result in results]

    return (
        bool(expected_text)
        and expected_text in answer_text
        and any(source in answer_text for source in source_names)
    )
