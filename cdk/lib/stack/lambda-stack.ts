import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { getAccountUniqueName } from "../config/accounts";
import { MoneybookStackProps } from "../moneybook-stack";
import { SYSTEM_NAME } from "../config/commons";
import { PythonFunction } from '@aws-cdk/aws-lambda-python-alpha';
import { CompositePrincipal, ManagedPolicy, Role, ServicePrincipal } from 'aws-cdk-lib/aws-iam';
import path = require('path');
import { Runtime } from 'aws-cdk-lib/aws-lambda';

export class MoneybookLambdaStack extends cdk.Stack {

    constructor(scope: Construct, id: string, props: MoneybookStackProps) {
        super(scope, id, props);

        // Lambda 함수에 할당할 IAM 역할(Role)을 생성
        const lambdaRole = new Role(this, `${SYSTEM_NAME}-lambda-role`, {
            roleName: `${getAccountUniqueName(props.context)}-lambda-rol`,
            // Lambda 서비스가 이 역할을 가정하여 실행
            assumedBy: new CompositePrincipal(
                new ServicePrincipal('lambda.amazonaws.com')
            ),
            // 기본 Lambda 실행 권한과 S3에 대한 완전한 액세스 권한을 부여
            managedPolicies: [
                ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole'),
                ManagedPolicy.fromAwsManagedPolicyName('AmazonS3FullAccess'),
            ],
        });

        // Python 런타임을 사용하는 Lambda 함수를 생성
        new PythonFunction(this, `${SYSTEM_NAME}-handler-file`, {
            functionName: `${getAccountUniqueName(props.context)}-handler-file`,
            handler: 'lambda_handler',
            entry: path.join(__dirname, '../../../app/backend'),
            index: 'lambda_handler.py',
            runtime: Runtime.PYTHON_3_10,
            role: lambdaRole,
            // Lambda 함수의 환경 변수로 S3 버킷 이름을 전달
            environment: {
                'BUCKET_NAME': props.s3Stack!.bucket.bucketName,
            },
        });
    }
}