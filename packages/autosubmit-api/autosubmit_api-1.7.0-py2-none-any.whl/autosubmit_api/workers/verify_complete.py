#!/usr/bin/env python
import autosubmit_api.experiment.common_requests as ExperimentUtils


def main():
    ExperimentUtils.verify_last_completed(1800)


if __name__ == "__main__":
    main()
