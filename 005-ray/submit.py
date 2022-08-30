from ray.job_submission import JobSubmissionClient, JobStatus
import time

client = JobSubmissionClient("http://localhost:8265")
job_id = client.submit_job(
    entrypoint="python script.py",
    runtime_env={
        'working_dir': './'  # 이게 있어야지 script.py 파일이 클러스터에 업로드 / 내부적으로 _upload_working_dir_if_needed 함수 호출
    }
)
print(job_id)


def wait_until_status(job_id, status_to_wait_for, timeout_seconds=5):
    start = time.time()
    while time.time() - start <= timeout_seconds:
        status = client.get_job_status(job_id)
        print(f"status: {status}")
        if status in status_to_wait_for:
            break
        time.sleep(1)


wait_until_status(job_id, {JobStatus.SUCCEEDED, JobStatus.STOPPED, JobStatus.FAILED})
logs = client.get_job_logs(job_id)
print(logs)
