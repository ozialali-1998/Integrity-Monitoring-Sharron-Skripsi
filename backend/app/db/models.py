from sqlalchemy import ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class MonitoredDirectory(Base):
    __tablename__ = "monitored_directories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    path: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[str] = mapped_column(Text, nullable=False)
    updated_at: Mapped[str] = mapped_column(Text, nullable=False)

    baseline_files: Mapped[list["BaselineFile"]] = relationship(back_populates="directory", cascade="all, delete-orphan")
    integrity_logs: Mapped[list["IntegrityLog"]] = relationship(back_populates="directory", cascade="all, delete-orphan")
    benchmark_results: Mapped[list["BenchmarkResult"]] = relationship(back_populates="directory")


class BaselineFile(Base):
    __tablename__ = "baseline_files"
    __table_args__ = (UniqueConstraint("monitored_directory_id", "relative_path", "algorithm", name="uq_baseline_files_directory_path_algorithm"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    monitored_directory_id: Mapped[int] = mapped_column(ForeignKey("monitored_directories.id", ondelete="CASCADE"), nullable=False)
    relative_path: Mapped[str] = mapped_column(Text, nullable=False)
    absolute_path: Mapped[str] = mapped_column(Text, nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    last_modified_at: Mapped[str | None] = mapped_column(Text, nullable=True)
    algorithm: Mapped[str] = mapped_column(Text, nullable=False)
    algorithm_params: Mapped[str | None] = mapped_column(Text, nullable=True)
    hash_value: Mapped[str] = mapped_column(Text, nullable=False)
    hash_duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    baseline_created_at: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[str] = mapped_column(Text, nullable=False)
    updated_at: Mapped[str] = mapped_column(Text, nullable=False)

    directory: Mapped[MonitoredDirectory] = relationship(back_populates="baseline_files")
    integrity_logs: Mapped[list["IntegrityLog"]] = relationship(back_populates="baseline_file")


class IntegrityLog(Base):
    __tablename__ = "integrity_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    monitored_directory_id: Mapped[int] = mapped_column(ForeignKey("monitored_directories.id", ondelete="CASCADE"), nullable=False)
    baseline_file_id: Mapped[int | None] = mapped_column(ForeignKey("baseline_files.id", ondelete="SET NULL"), nullable=True)
    event_type: Mapped[str] = mapped_column(Text, nullable=False)
    relative_path: Mapped[str] = mapped_column(Text, nullable=False)
    previous_hash: Mapped[str | None] = mapped_column(Text, nullable=True)
    current_hash: Mapped[str | None] = mapped_column(Text, nullable=True)
    previous_size_bytes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    current_size_bytes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    previous_modified_at: Mapped[str | None] = mapped_column(Text, nullable=True)
    current_modified_at: Mapped[str | None] = mapped_column(Text, nullable=True)
    severity: Mapped[str] = mapped_column(Text, nullable=False, default="INFO")
    status: Mapped[str] = mapped_column(Text, nullable=False, default="OPEN")
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    checked_at: Mapped[str] = mapped_column(Text, nullable=False)
    verification_duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[str] = mapped_column(Text, nullable=False)

    directory: Mapped[MonitoredDirectory] = relationship(back_populates="integrity_logs")
    baseline_file: Mapped[BaselineFile | None] = relationship(back_populates="integrity_logs")


class BenchmarkResult(Base):
    __tablename__ = "benchmark_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    monitored_directory_id: Mapped[int | None] = mapped_column(ForeignKey("monitored_directories.id", ondelete="SET NULL"), nullable=True)
    algorithm: Mapped[str] = mapped_column(Text, nullable=False)
    algorithm_params: Mapped[str | None] = mapped_column(Text, nullable=True)
    total_files: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_size_bytes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_duration_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    average_duration_ms: Mapped[float | None] = mapped_column(nullable=True)
    min_duration_ms: Mapped[float | None] = mapped_column(nullable=True)
    max_duration_ms: Mapped[float | None] = mapped_column(nullable=True)
    throughput_mb_per_sec: Mapped[float | None] = mapped_column(nullable=True)
    verification_duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    accuracy_percent: Mapped[float | None] = mapped_column(nullable=True)
    verification_matches: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    verification_mismatches: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    average_cpu_percent: Mapped[float | None] = mapped_column(nullable=True)
    max_cpu_percent: Mapped[float | None] = mapped_column(nullable=True)
    memory_start_bytes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    memory_end_bytes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    memory_peak_bytes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    benchmark_started_at: Mapped[str] = mapped_column(Text, nullable=False)
    benchmark_finished_at: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[str] = mapped_column(Text, nullable=False)

    directory: Mapped[MonitoredDirectory | None] = relationship(back_populates="benchmark_results")


class SystemSetting(Base):
    __tablename__ = "system_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    setting_key: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    setting_value: Mapped[str] = mapped_column(Text, nullable=False)
    value_type: Mapped[str] = mapped_column(Text, nullable=False, default="string")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_editable: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[str] = mapped_column(Text, nullable=False)
    updated_at: Mapped[str] = mapped_column(Text, nullable=False)
