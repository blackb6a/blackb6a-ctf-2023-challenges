#!/usr/bin/env bash
set -e

S3_TARGET_BUCKET="chalfileserverstack-filesbucket16450113-1rblq08n5nw5f"

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd "$SCRIPT_DIR/../"
aws s3 sync ./build/public "s3://$S3_TARGET_BUCKET"
