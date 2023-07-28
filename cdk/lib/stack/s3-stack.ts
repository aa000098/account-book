import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';
import { Construct } from 'constructs';
import { MoneybookStackProps } from '../moneybook-stack';
import { getAccountUniqueName, Account } from '../config/accounts';
import { SYSTEM_NAME } from "../config/commons";

export class MoneybookS3Stack extends cdk.Stack {
    // 생성된 S3 버킷 인스턴스 저장할 프로퍼티
    public bucket: s3.IBucket

    constructor(scope: Construct, id: string, props: MoneybookStackProps) {
        super(scope, id, props);

        // S3 버킷 생성
        const bucket = new s3.Bucket(this, `${SYSTEM_NAME}-S3`, {
            // 사용자 고유한 이름과 "moneybook-bucket"을 조합하여 유니크한 버킷 이름을 생성
            bucketName: `${getAccountUniqueName(props.context)}-moneybook-bucket`.toLowerCase(),
            // 버킷에 대한 공개 읽기 권한을 차단
            publicReadAccess: false,
            // 모든 공개 액세스를 차단
            blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
            // S3에서 제공하는 관리형 암호화를 사용하여 데이터를 암호화
            encryption: s3.BucketEncryption.S3_MANAGED,
        });

        // 생성된 S3 버킷 인스턴스를 프로퍼티에 저장
        this.bucket = bucket;
    }
}