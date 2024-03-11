-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 02, 2023 at 11:47 AM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `fidia`
--

-- --------------------------------------------------------

--
-- Table structure for table `api_block`
--

CREATE TABLE `api_block` (
  `index` int(11) NOT NULL,
  `hash` longtext NOT NULL,
  `transaction` longtext NOT NULL,
  `block_type` longtext NOT NULL,
  `previous_hash` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `api_block`
--

INSERT INTO `api_block` (`index`, `hash`, `transaction`, `block_type`, `previous_hash`, `created_at`) VALUES
(1, '541963a34346a1880a17157517a707e582d79fb8cfb7472074be88d93aabc88e', 'First Block', 'Genesis block', '0', '2023-06-02 07:08:22.028406'),
(2, '9ec35ba83086be230b58a13f0d4d9f3ab3f2828e0658f7af138c15bfa3e5d767', '{\"type\": \"User\", \"id\": 1, \"name\": \"test\", \"email\": \"test@gmail.com\", \"mobile\": \"1234567890\", \"city\": \"mysore\", \"country\": \"india\"}', 'Create user', '541963a34346a1880a17157517a707e582d79fb8cfb7472074be88d93aabc88e', '2023-06-02 07:24:12.024936'),
(3, 'c7572c229b1797d178bbc4dc6583f40f08af3bf222b00b062115cc002f748c59', '{\"userid\": 1}', 'Private Key Generation', '9ec35ba83086be230b58a13f0d4d9f3ab3f2828e0658f7af138c15bfa3e5d767', '2023-06-02 07:27:43.760801'),
(4, '24f08ab4eede0a252ef97cc9643cd7117d78cf6d8ebb0a2fe69c0e8c273d8590', '{\"id\": 1, \"userid\": \"1\", \"cloudname\": \"cloud1\", \"filename\": \"garden.png\"}', 'File upload', 'c7572c229b1797d178bbc4dc6583f40f08af3bf222b00b062115cc002f748c59', '2023-06-02 07:28:37.115689');

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(9, 'api', 'block'),
(1, 'contenttypes', 'contenttype'),
(7, 'fidia', 'auditrequest'),
(3, 'fidia', 'cloud'),
(8, 'fidia', 'fileuploads'),
(4, 'fidia', 'kgc'),
(5, 'fidia', 'tpa'),
(6, 'fidia', 'user'),
(2, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2022-05-04 16:53:01.112393'),
(2, 'contenttypes', '0002_remove_content_type_name', '2022-05-04 16:53:02.119068'),
(3, 'sessions', '0001_initial', '2022-05-04 16:53:02.684324'),
(4, 'fidia', '0001_initial', '2022-05-04 17:00:29.844179'),
(5, 'fidia', '0002_user_biometricimage', '2022-05-04 18:08:28.149225'),
(6, 'fidia', '0003_alter_user_status', '2022-05-05 04:48:30.551652'),
(7, 'fidia', '0004_user_privatekey', '2022-05-05 05:39:19.091717'),
(8, 'fidia', '0005_alter_user_privatekey', '2022-05-05 10:44:25.781648'),
(9, 'fidia', '0006_auditrequest_fileuploads', '2022-05-05 12:02:22.687950'),
(10, 'fidia', '0007_fileuploads_key', '2022-05-05 14:29:13.627195'),
(11, 'fidia', '0008_alter_auditrequest_cloudauditat_and_more', '2022-05-05 14:51:41.961101'),
(12, 'fidia', '0009_rename_tap_tpa', '2022-05-05 15:27:45.300982'),
(13, 'fidia', '0010_alter_fileuploads_key', '2022-05-05 16:36:45.188970'),
(14, 'api', '0001_initial', '2023-06-02 07:07:09.276189'),
(15, 'api', '0002_alter_block_transaction', '2023-06-02 07:07:09.420356');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('3gji1okqu6i2io336c8c6dlbwj05nkhj', 'e30:1q51Mx:qx2DMi_VZWwYuDnhFerYnu59VD24uQLzLYoAC19sR1g', '2023-06-16 09:46:51.338916'),
('efto4bccgpyu6zulneev8jgj3qr2b7sh', 'e30:1nqI27:Zn6OdMZoq_9vpX3TZ9wqGadYna4ZCXMQOF7o_TECvEw', '2022-05-29 17:27:55.569998'),
('vn5q3quqtxlkf7lgdsb69q7254l40kvi', 'e30:1nnjuo:Ntdh97pC2KdJO_Z1gyKPeGKo7-3hUetZtf3pjW0W4Tk', '2022-05-22 16:37:50.629993'),
('w0q3qlv94qw4u10mspd5q68fgc7tz298', 'e30:1nnc5y:wajr9BRwO7caKgJPz52lBA0dIbANXDdwIKNtdNu51ME', '2022-05-22 08:16:50.562341');

-- --------------------------------------------------------

--
-- Table structure for table `fidia_auditrequest`
--

CREATE TABLE `fidia_auditrequest` (
  `id` int(11) NOT NULL,
  `userid` int(11) NOT NULL,
  `fileid` int(11) NOT NULL,
  `tpastatus` int(11) NOT NULL,
  `tpaat` datetime(6) DEFAULT NULL,
  `cloudstatus` int(11) NOT NULL,
  `cloudauditat` datetime(6) DEFAULT NULL,
  `cloudhashresult` longtext DEFAULT NULL,
  `tpaverification` int(11) NOT NULL,
  `tpaverifiedat` datetime(6) DEFAULT NULL,
  `userverification` int(11) NOT NULL,
  `userverifiedat` datetime(6) DEFAULT NULL,
  `creationDate` datetime(6) NOT NULL,
  `UpdationDate` datetime(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `fidia_cloud`
--

CREATE TABLE `fidia_cloud` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `fidia_cloud`
--

INSERT INTO `fidia_cloud` (`id`, `username`, `password`) VALUES
(1, 'cloud', 'ceb6c970658f31504a901b89dcd3e461');

-- --------------------------------------------------------

--
-- Table structure for table `fidia_fileuploads`
--

CREATE TABLE `fidia_fileuploads` (
  `id` int(11) NOT NULL,
  `userid` int(11) NOT NULL,
  `filename` varchar(200) NOT NULL,
  `hashcode` longtext NOT NULL,
  `cloudname` varchar(200) NOT NULL,
  `creationDate` datetime(6) NOT NULL,
  `UpdationDate` datetime(6) DEFAULT NULL,
  `key` longblob NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `fidia_fileuploads`
--

INSERT INTO `fidia_fileuploads` (`id`, `userid`, `filename`, `hashcode`, `cloudname`, `creationDate`, `UpdationDate`, `key`) VALUES
(1, 1, 'garden.png', '8c0b991d208564903cec3397a76b4a9f379c1aeb241f763fc0dafdce7b61ef5e', 'cloud1', '2023-06-02 07:28:35.035206', '2023-06-02 07:28:37.164556', 0x375931547446522d68504c66737a516f51374a6a466a526237666248424d7857565553586f4258664934303d);

-- --------------------------------------------------------

--
-- Table structure for table `fidia_kgc`
--

CREATE TABLE `fidia_kgc` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `fidia_kgc`
--

INSERT INTO `fidia_kgc` (`id`, `username`, `password`) VALUES
(1, 'kgc', 'ceb6c970658f31504a901b89dcd3e461');

-- --------------------------------------------------------

--
-- Table structure for table `fidia_tpa`
--

CREATE TABLE `fidia_tpa` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `fidia_tpa`
--

INSERT INTO `fidia_tpa` (`id`, `username`, `password`) VALUES
(1, 'tpa', 'ceb6c970658f31504a901b89dcd3e461');

-- --------------------------------------------------------

--
-- Table structure for table `fidia_user`
--

CREATE TABLE `fidia_user` (
  `id` int(11) NOT NULL,
  `fullname` varchar(20) NOT NULL,
  `email` varchar(50) NOT NULL,
  `mobile` varchar(20) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `birthdate` date NOT NULL,
  `status` int(11) NOT NULL,
  `password` varchar(200) NOT NULL,
  `country` varchar(200) NOT NULL,
  `city` varchar(200) NOT NULL,
  `biometricimage` longtext NOT NULL,
  `privatekey` longtext DEFAULT NULL,
  `creationDate` datetime(6) NOT NULL,
  `UpdationDate` datetime(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `fidia_user`
--

INSERT INTO `fidia_user` (`id`, `fullname`, `email`, `mobile`, `gender`, `birthdate`, `status`, `password`, `country`, `city`, `biometricimage`, `privatekey`, `creationDate`, `UpdationDate`) VALUES
(1, 'test', 'test@gmail.com', '1234567890', 'male', '1988-03-03', 1, 'f925916e2754e5e03f75dd58a5733251', 'india', 'mysore', '1.png', 'c8ee83a527c5466a7afc679019e90e7258437af8b9204c5efb0f2b8c2f1297f8', '2023-06-02 07:24:09.951510', '2023-06-02 07:27:41.669247');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `api_block`
--
ALTER TABLE `api_block`
  ADD PRIMARY KEY (`index`),
  ADD UNIQUE KEY `hash` (`hash`) USING HASH,
  ADD UNIQUE KEY `previous_hash` (`previous_hash`) USING HASH;

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `fidia_auditrequest`
--
ALTER TABLE `fidia_auditrequest`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `fidia_cloud`
--
ALTER TABLE `fidia_cloud`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `fidia_fileuploads`
--
ALTER TABLE `fidia_fileuploads`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `fidia_kgc`
--
ALTER TABLE `fidia_kgc`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `fidia_tpa`
--
ALTER TABLE `fidia_tpa`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `fidia_user`
--
ALTER TABLE `fidia_user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `api_block`
--
ALTER TABLE `api_block`
  MODIFY `index` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `fidia_auditrequest`
--
ALTER TABLE `fidia_auditrequest`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `fidia_cloud`
--
ALTER TABLE `fidia_cloud`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `fidia_fileuploads`
--
ALTER TABLE `fidia_fileuploads`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `fidia_kgc`
--
ALTER TABLE `fidia_kgc`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `fidia_tpa`
--
ALTER TABLE `fidia_tpa`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `fidia_user`
--
ALTER TABLE `fidia_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
